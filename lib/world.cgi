sub begin { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ﾌﾟﾛｸﾞﾗﾑｴﾗｰ異常な処理です'); }
sub tp_1  { &refresh; $m{shogo}=$shogos[1][0]; &write_user; &error('ﾌﾟﾛｸﾞﾗﾑｴﾗｰ異常な処理です'); }
require './lib/_world_reset.cgi';
#================================================
# 世界情勢 Created by Merino
#================================================

#================================================
# 選択画面
#================================================
sub tp_100 {
	$mes .= "あなたはこの世界に何を求めますか?<br>";
	&menu('皆が望むもの','希望','絶望','平和');
	$m{tp} += 10;
}

sub tp_110 {
	my $old_world = $w{world};

	&show_desire;
	if (&is_special_world($w{world})) {# 特殊情勢ならば
		if ($old_world eq $#world_states) {# 暗黒開始メッセージ
			&write_world_news("<i>$m{name}の願いはかき消されました</i>");
		}
		elsif ($old_world eq $#world_states-1) {# 混乱開始メッセージ
			&write_world_news("<i>$m{name}の願いは空しく世界は混乱に陥りました</i>");
		}
		elsif ($old_world eq $#world_states-2) {# 紅白開始メッセージ
			&write_world_news("<i>$m{name}の願いは空しく世界は二つに分かれました</i>");
		}
		elsif ($old_world eq $#world_states-3) {# 三国志開始メッセージ
			&write_world_news("<i>$m{name}の願いも空しく分裂した世界を統一すべく三国が台頭しました</i>");
		}
		elsif ($old_world eq $#world_states-4) {# 英雄開始メッセージ
			&write_world_news("<i>$m{name}の願いは空しく世界は英雄が伝説を作り出す時代になりました</i>");
		}
		elsif ($old_world eq $#world_states-5) {# 拙速開始メッセージ
			&write_world_news("<i>$m{name}の願いも空しく世界が競い合うことに</i>");
		}
	}
	else {# 特殊情勢ではないならば
		my @new_worlds;
		if ($cmd eq '1') { # 希望
			@new_worlds = (1,2,3,4,5,6,7,17,18,19,20);
		}
		elsif ($cmd eq '2') { # 絶望
			@new_worlds = (8,9,10,11,12,13,14,15,16);
		}
		elsif ($cmd eq '3') { # 平和
			@new_worlds = (0);
		}
		else {
			@new_worlds = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);
		}
	
		my @next_worlds = &unique_worlds(@new_worlds);
		$w{world} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];
		$w{world_sub} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];

		# 同じのじゃつまらないので
		if ($w{world} eq $old_world) {
			$w{world} = int(rand($#world_states-5));
			++$w{world} if $w{world} eq $old_world;
			$w{world} = int(rand(10)) if $w{world} >= $#world_states-5;
			&write_world_news("<i>世界は $world_states[$old_world] となりま…せん $world_states[$w{world}]となりました</i>");
		}
		else {
			if ($w{world} eq '0') {# 平和
				&write_world_news("<i>世界は $world_states[$w{world}] になりました</i>");
			}
			elsif ($w{world} eq '18') {# 殺伐
				&write_world_news("<i>世界は $world_states[$w{world}] としたふいんき(←なぜか変換できない)になりました</i>");
			}
			else {
				&write_world_news("<i>世界は $world_states[$w{world}] となりました</i>");
			}
		}
	}

	unshift @old_worlds, $w{world};
	open my $fh, "> $logdir/world_log.cgi" or &error("$logdir/world_log.cgiが開けません");
	my $saved_w = 0;
	$nline = "";
	for my $old_w (@old_worlds){
		next if $old_w =~ /[^0-9]/;
		$nline .= "$old_w<>";
		last if $saved_w > 15;
		$saved_w++;
	}
	print $fh "$nline\n";
	close $fh;

	my $migrate_type = 0;
	if ($w{world} eq '0') { # 平和
		$w{reset_time} += 3600 * 12;
	}
	elsif ($w{world} eq '6') { # 結束
		my @win_cs = ();
		for my $i (1 .. $w{country}) {
			push @win_cs, [$i, $cs{win_c}[$i]];
		}
		@win_cs = sort { $b->[1] <=> $a->[1] } @win_cs;
		
		# 奇数の場合は一番国は除く
		shift @win_cs if @win_cs % 2 == 1;
		
		my $half_c = int(@win_cs*0.5-1);
		for my $i (0 .. $half_c) {
			my $c_c = &union($win_cs[$i][0],$win_cs[$#win_cs-$i][0]);
			$w{'p_'.$c_c} = 1;
		}
	}
	elsif ($w{world} eq '18') { # 殺伐
		$w{reset_time} = $time;
		for my $i (1 .. $w{country}) {
			$cs{food}[$i]     = int(rand(300)) * 1000;
			$cs{money}[$i]    = int(rand(300)) * 1000;
			$cs{soldier}[$i]  = int(rand(300)) * 1000;
		}
	}
	elsif (&is_festival_world($w{world})) {
		if ($w{world} eq $#world_states-4) { # 英雄
			$w{game_lv} += 20;
			for my $i (1 .. $w{country}) {
				$cs{strong}[$i]     = int(rand(15) + 25) * 1000;
			}
		}
		elsif ($w{world} eq $#world_states-2) { # 不倶戴天
			$w{game_lv} = 99;
			$migrate_type = add_festival_country('kouhaku');
		}
		elsif ($w{world} eq $#world_states-3) { # 三国志
			$w{game_lv} = 99;
			$migrate_type = add_festival_country('sangokusi');
		}
		elsif ($w{world} eq $#world_states-5) { # 拙速
			$migrate_type = festival_type('sessoku', 1);
		}
		elsif ($w{world} eq $#world_states-1) { # 混乱
			$migrate_type = festival_type('konran', 1);
		}
	}
	
	$w{game_lv} = $w{world} eq '15' || $w{world} eq '17' ? int($w{game_lv} * 0.7):$w{game_lv};
	
	&refresh;
	&n_menu;
	&write_cs;
	
	require "./lib/reset.cgi";
	&player_migrate($migrate_type);
}

# プレイヤーの望みを表示する
sub show_desire {
	if ($cmd eq '1') { # 希望
		&mes_and_world_news("<b>世界に希望を望みました</b>", 1);
	}
	elsif ($cmd eq '2') { # 絶望
		&mes_and_world_news("<b>世界に絶望を望みました</b>", 1);
	}
	elsif ($cmd eq '3') { # 平和
		&mes_and_world_news("<b>世界に平和を望みました</b>", 1);
	}
	else {
		&mes_and_world_news('<b>世界にみなが望むものを望みました</b>', 1);
	}
}

1; # 削除不可

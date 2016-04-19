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
	# 統一時worldと期限切れ時resetで対にしたかったが統一者の画面にも表示するため断念
	# 特殊情勢における統一時の文言は _war_result.cgi を書き換える

	# 祭り情勢時に統一
	if (&is_festival_world) {
		if ($w{world} eq $#world_states-1) { # 混乱
			$migrate_type = &festival_type('konran', 0);
		}
		elsif ($w{world} eq $#world_states-2) { # 不倶戴天
			$migrate_type = &festival_type('kouhaku', 0);
			$w{country} -= 2;
		}
		elsif ($w{world} eq $#world_states-3) { # 三国志
			$migrate_type = &festival_type('sangokusi', 0);
			$w{country} -= 3;
		}
		&player_migrate($migrate_type);
	}
	elsif (&is_special_world) {
		require './lib/reset.cgi';
		&reset;
	}

	$mes .= "あなたはこの世界に何を求めますか?<br>";
	&menu('皆が望むもの','希望','絶望','平和');
	$m{tp} += 10;
}

sub tp_110 {
	my $old_world = $w{world};

	&show_desire unless $w{year} =~ /5$/;
	if ($w{year} =~ /9$/) { # 祭り情勢開始時
		my $year = $w{year} + 1;
		if ($year % 40 == 0) { # 不倶戴天
			&write_world_news("<i>$m{name}の願いは空しく世界は二つに分かれました</i>");
		}
		elsif ($year % 40 == 20) { # 三国志
			&write_world_news("<i>$m{name}の願いも空しく分裂した世界を統一すべく三国が台頭しました</i>");
		}
		elsif ($year % 40 == 10) { # 拙速
			&write_world_news("<i>$m{name}の願いも空しく世界が競い合うことに</i>");
		}
		else { # 混乱
			&write_world_news("<i>$m{name}の願いは空しく世界は混乱に陥りました</i>");
		}
	}
	elsif (!$w{year} =~ /5$/) {# 特殊情勢開始時ではない
		my @new_worlds;
		if ($cmd eq '1') {# 希望
			@new_worlds = (1,2,3,4,5,6,7,17,18,19,20);
		}
		elsif ($cmd eq '2') {# 絶望
			@new_worlds = (8,9,10,11,12,13,14,15,16);
		}
		elsif ($cmd eq '3') {# 平和
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
		$w{game_lv} = int($w{game_lv} * 0.7) if $w{world} eq '15' || $w{world} eq '17';
	}# else {# 特殊情勢開始時ではない

	require './lib/reset.cgi';
	&reset; # ここまで今期統一時の処理

	my $migrate_type = 0;
	# 世界情勢 混乱突入
	if ($w{year} =~ /6$/) { # 暗黒・英雄
		&show_desire;
		&write_world_news("<i>$m{name}の願いはかき消されました</i>");
	}
	elsif ($w{year} =~ /0$/) {
		require './lib/_festival_world.cgi';
		$migrate_type = &opening_festival;
		&wt_c_reset;
	}

#	unshift @old_worlds, $w{world};
	open my $fh, "> $logdir/world_log.cgi" or &error("$logdir/world_log.cgiが開けません");
	my $saved_w = 0;
	$nline = "";
	for my $old_w (@old_worlds){
		next if $old_w =~ /[^0-9]/;
		$nline .= "$old_w<>";
		last if $saved_w > 15;
		$saved_w++;
	}
	print $fh "$w{world}<>$nline\n";
	close $fh;

#	my $migrate_type = 0;
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
#	elsif (&is_festival_world) {# 祭り情勢ならば
#		if ($w{world} eq $#world_states-1) { # 混乱
#			$migrate_type = &festival_type('konran', 1);
#		}
#		elsif ($w{world} eq $#world_states-2) { # 不倶戴天
#			$w{game_lv} = 99;
#			$migrate_type = &add_festival_country('kouhaku');
#		}
#		elsif ($w{world} eq $#world_states-3) { # 三国志
#			$w{game_lv} = 99;
#			$migrate_type = &add_festival_country('sangokusi');
#		}
#		elsif ($w{world} eq $#world_states-4) { # 英雄
#			$w{game_lv} += 20;
#			for my $i (1 .. $w{country}) {
#				$cs{strong}[$i]     = int(rand(15) + 25) * 1000;
#			}
#		}
#		elsif ($w{world} eq $#world_states-5) { # 拙速
#			$migrate_type = &festival_type('sessoku', 1);
#		}
#	}

	$w{game_lv} = 0;
	&refresh;
	&n_menu;
	&write_cs;

#	require "./lib/reset.cgi";
#	&player_migrate($migrate_type);
	&player_migrate($migrate_type) if &is_festival_world;
}

# プレイヤーの望みを表示する
sub show_desire {
	if ($cmd eq '1') {# 希望
		&mes_and_world_news("<b>世界に希望を望みました</b>", 1);
	}
	elsif ($cmd eq '2') {# 絶望
		&mes_and_world_news("<b>世界に絶望を望みました</b>", 1);
	}
	elsif ($cmd eq '3') {# 平和
		&mes_and_world_news("<b>世界に平和を望みました</b>", 1);
	}
	else {
		&mes_and_world_news('<b>世界にみなが望むものを望みました</b>', 1);
	}
}

1; # 削除不可
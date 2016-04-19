use File::Copy::Recursive qw(rcopy);
use File::Path;
require './lib/_world_reset.cgi';
require './lib/_festival_world.cgi';
#================================================
# 国ﾘｾｯﾄ Created by Merino
#================================================

# 統一難易度：[難しい 60 〜 40 簡単]
my $game_lv = $config_test ? int(rand(6) + 5) : int( rand(11) + 40 );

# 統一期限(日)
my $limit_touitu_day = int( rand(6)+5 );

#================================================
# 期日が過ぎた場合
#================================================
sub time_limit {
	# 祭り情勢時に期限切れ
	if (&is_special_world) {
		if ($w{world} eq $#world_states-5) { # 拙速
			my $strongest_country = 0;
			my $max_value = 0;
			for my $i (1 .. $w{country}) {
				if ($cs{strong}[$i] > $max_value) {
					$strongest_country = $i;
					$max_value = $cs{strong}[$i];
				}
			}
			&write_world_news("<b>$world_name大陸を全土にわたる国力競争は$cs{name}[$strongest_country]の勝利になりました</b>");
			&write_legend('touitu', "$world_name大陸を全土にわたる国力競争は$cs{name}[$strongest_country]の勝利になりました");
			$w{win_countries} = $strongest_country;
		}
		else {
			&write_world_news("<b>$world_name大陸を統一する者は現れませんでした</b>");
			&write_legend('touitu', "$world_name大陸を統一する者は現れませんでした");
		}
		$w{world} = int(rand($#world_states-5));
		&write_world_news("<i>世界は $world_states[$w{world}] となりました</i>");
#		&player_migrate($migrate_type);
	}
	else { # 通常情勢で期限切れ
		&write_world_news("<b>$world_name大陸を統一する者は現れませんでした</b>");
		&write_legend('touitu', "$world_name大陸を統一する者は現れませんでした");
		$w{win_countries} = '';

		# 特殊情勢前期ではないなら
		unless ($w{year} =~ /5$/ || $w{year} =~ /9$/) {
			my @new_worlds = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);
			my @next_worlds = &unique_worlds(@new_worlds);
			$w{world} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];
#			&write_world_news("<i>世界は $world_states[$w{world}] となりました</i>");
		}
#			my $year = $w{year} + 1;
#			if ($year =~ /06$/ || $year =~ /26$/ || $year =~ /46$/ || $year =~ /66$/ || $year =~ /86$/) { # 英雄
#				&write_world_news("<i>世界は $world_states[$#world_states-4] となりました</i>");
#			}
#			elsif ($w{year} =~ /5$/) { # 暗黒
##				&write_world_news("<i>世界は $world_states[$#world_states] となりました</i>");
#			}
#			elsif ($year % 40 == 0) { # 不倶戴天
#				&write_world_news("<i>世界は $world_states[$#world_states-2] となりました</i>");
#			}
#			elsif ($year % 40 == 20) { # 三国志
#				&write_world_news("<i>世界は $world_states[$#world_states-3] となりました</i>");
#			}
#			elsif ($year % 40 == 10) { # 拙速
#				&write_world_news("<i>世界は $world_states[$#world_states-5] となりました</i>");
#			}
#			else { # 混乱
#				&write_world_news("<i>世界は $world_states[$#world_states-1] となりました</i>");
#			}
#		}
#		else {
#			unless ($w{year} =~ /5$/ || $w{year} =~ /6$/) {
#			}
#			if ($w{year} =~ /6$/) { # 暗黒終了時なら
#				$w{world} = int(rand($#world_states-5));
#			}
#			else {
#				my @new_worlds = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);
#				my @next_worlds = &unique_worlds(@new_worlds);
#				$w{world} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];
#			}

#			&write_world_news("<i>世界は $world_states[$w{world}] となりました</i>");
#		}
	}

	&reset; # ここまで今期期限切れ時の処理

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

	if ($w{world} eq '0') {# 平和
		&write_world_news("<i>世界は $world_states[$w{world}] になりました</i>");
	}
	elsif ($w{world} eq '18') {# 殺伐
		&write_world_news("<i>世界は $world_states[$w{world}] としたふいんき(←なぜか変換できない)になりました</i>");
	}
	else {
		&write_world_news("<i>世界は $world_states[$w{world}] となりました</i>");
	}

#			my $year = $w{year} + 1;
#			if ($year =~ /06$/ || $year =~ /26$/ || $year =~ /46$/ || $year =~ /66$/ || $year =~ /86$/) { # 英雄
#				&write_world_news("<i>世界は $world_states[$#world_states-4] となりました</i>");
#			}
#			elsif ($w{year} =~ /5$/) { # 暗黒
##				&write_world_news("<i>世界は $world_states[$#world_states] となりました</i>");
#			}
#			elsif ($year % 40 == 0) { # 不倶戴天
#				&write_world_news("<i>世界は $world_states[$#world_states-2] となりました</i>");
#			}
#			elsif ($year % 40 == 20) { # 三国志
#				&write_world_news("<i>世界は $world_states[$#world_states-3] となりました</i>");
#			}
#			elsif ($year % 40 == 10) { # 拙速
#				&write_world_news("<i>世界は $world_states[$#world_states-5] となりました</i>");
#			}
#			else { # 混乱
#				&write_world_news("<i>世界は $world_states[$#world_states-1] となりました</i>");
#			}
#		}
#		else {
#			unless ($w{year} =~ /5$/ || $w{year} =~ /6$/) {
#			}
#			if ($w{year} =~ /6$/) { # 暗黒終了時なら
#				$w{world} = int(rand($#world_states-5));
#			}
#			else {
#				my @new_worlds = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20);
#				my @next_worlds = &unique_worlds(@new_worlds);
#				$w{world} = @next_worlds == 0 ? 0:$next_worlds[int(rand(@next_worlds))];
#			}

#			&write_world_news("<i>世界は $world_states[$w{world}] となりました</i>");
#		}
#	}

#	my $migrate_type = 0;
#	# 世界情勢 混乱突入
#	if ($w{year} =~ /0$/) {
#		require './lib/_festival_world.cgi';
#		$migrate_type = &opening_festival;
#		&wt_c_reset;
#	}

#	unshift @old_worlds, $w{world};

#	elsif ($w{world} eq $#world_states) { # 暗黒ならば
#		&write_world_news("<i>世界は $world_states[$w{world}] となりました</i>");
#	}
#	elsif ($w{world} eq $#world_states-4) { # 英雄
#		$w{game_lv} += 20;
#		for my $i (1 .. $w{country}) {
#			$cs{strong}[$i]     = int(rand(15) + 25) * 1000;
#		}
#	}

	$w{game_lv} = 0;

	&write_cs;
#	&player_migrate($migrate_type) if &is_festival_world;
}

#================================================
# 国ﾃﾞｰﾀﾘｾｯﾄ処理
# 統一と期限切れで呼ばれるので抽象的とする
# reset後に情勢が確定するため、ここを通ってから情勢を表示すること
#================================================
sub reset {
	require './lib/casino_toto.cgi';
	&pay_back($w{year});

	# reset countries
	for my $i (1 .. $w{country}) {
		$cs{strong}[$i] = 8000;
	}

	# 終了処理
	if (&is_special_world) { # 特殊情勢終了
		if ($w{year} =~ /6$/) { # 暗黒・英雄終了
			unless ($w{year} =~ /06$/ || $w{year} =~ /26$/ || $w{year} =~ /46$/ || $w{year} =~ /66$/ || $w{year} =~ /86$/) { # 暗黒終了
				require './lib/vs_npc.cgi';
				&delete_npc_country;
			}
			# 英雄終了処理は特になし
		}
		else { # 祭り情勢終了
			require './lib/_festival_world.cgi';
			my $migrate_type = &ending_festival;
			&player_migrate($migrate_type);
		}
#		$w{world} = int(rand($#world_states-5));
	}

	# 世界情勢 暗黒解除
#	if ($w{year} =~ /6$/) {
#		$w{world} = int(rand($#world_states-5));
#		if ($w{year} =~ /06$/ || $w{year} =~ /26$/ || $w{year} =~ /46$/ || $w{year} =~ /66$/ || $w{year} =~ /86$/) {
#			$w{world} = int(rand($#world_states-5));
#		} else {
#			require './lib/vs_npc.cgi';
#			&delete_npc_country;
#			$w{world} = int(rand($#world_states-5));
#		}
		# 統一→resetでランダム情勢→ユーザーが情勢決定
		# ユーザーが情勢を選ばない限り暗黒が続くので仕方ないか？
#		&write_world_news("<i>世界は $world_states[$w{world}] となりました</i>");
#	}
#	# 世界情勢 混乱解除
#	if ($w{year} =~ /0$/) {
#		if($w{year} % 40 == 0){#不倶戴天
#			$migrate_type = &festival_type('kouhaku', 0);
#			$w{country} -= 2;
#		}elsif($w{year} % 40 == 20){# 三国志
#			$migrate_type = &festival_type('sangokusi', 0);
#			$w{country} -= 3;
#		}elsif($w{year} % 40 == 10){# 拙速
#			$migrate_type = &festival_type('sessoku', 0);
#		}else {#混乱
#			$migrate_type = &festival_type('konran', 0);
#		}
#		$w{world} = int(rand($#world_states-5));
#		# とりあえずユーザーが情勢を選ぶ余地がない拙速だけ表示
#		# おそらく統一期限切れでここを通っているなら他の祭り情勢でも表示しないと今度は何も表示されない
#		# 戦争で統一したのか期限切れなのか要判断
#		&write_world_news("<i>世界は $world_states[$w{world}] となりました</i>") if $w{year} % 40 == 10;
#	}
	# 仕官できる人数
	my $country = $w{world} eq $#world_states ? $w{country} - 1 : $w{country};
	my $ave_c = int($w{player} / $country);

	# set world
	$w{year}++;
	$w{reset_time} = $config_test ? $time : $time + 3600 * 8; #12
#	$w{limit_time} = $time + 3600 * 24 * $limit_touitu_day;
	$w{limit_time} = $config_test ? $time: $time + 3600 * 24 * $limit_touitu_day;
	$w{game_lv} = $game_lv;
	if($w{year} % 40 == 10){
		$w{reset_time} = $config_test ? $time: $time + 3600 * 12;
		$w{limit_time} = $config_test ? $time: $time + 3600 * 36;
		$w{game_lv} = 99;
	}
	
	my($c1, $c2) = split /,/, $w{win_countries};

	# set countries
	for my $i (1 .. $w{country}) {
		# 統一国の場合はNPC弱体
		if($w{year} % 40 == 10){
			$cs{strong}[$i] = 5000;
			$cs{tax}[$i] = 99;
			$cs{state}[$i] = 5;
		} else {
			$cs{strong}[$i] = $c1 eq $i || $c2 eq $i ? 8000 : int(rand(6) + 10) * 1000;
			$cs{state}[$i]    = rand(2) > 1 ? 0 : int(rand(@country_states));
		}
		$cs{food}[$i]     = int(rand(30) + 5) * 1000;
		$cs{money}[$i]    = int(rand(30) + 5) * 1000;
		$cs{soldier}[$i]  = int(rand(30) + 5) * 1000;
		$cs{capacity}[$i] = $ave_c;
		$cs{is_die}[$i]   = 0;
		$cs{modify_war}[$i]   = 0;
		$cs{modify_dom}[$i]   = 0;
		$cs{modify_mil}[$i]   = 0;
		$cs{modify_pro}[$i]   = 0;
		
		for my $j ($i+1 .. $w{country}) {
			$w{ "f_${i}_${j}" } = int(rand(40));
			$w{ "p_${i}_${j}" } = 0;
		}
		
		if ($w{year} % $reset_ceo_cycle_year == 0) {
			if ($cs{ceo}[$i]) {
				my $n_id = unpack 'H*', $cs{ceo}[$i];
				open my $fh, ">> $userdir/$n_id/ex_c.cgi";
				print $fh "ceo_c<>1<>\n";
				close $fh;
			}
			$cs{ceo}[$i] = '';
			
			open my $fh, "> $logdir/$i/leader.cgi";
			close $fh;
		}
		
		if ($w{year} % $reset_daihyo_cycle_year == 0) {
			for my $k (qw/war dom pro mil/) {
				my $kc = $k . "_c";
				next if $cs{$k}[$i] eq '';
				my $trick_id = unpack 'H*', $cs{$k}[$i];
				my %datas = &get_you_datas($trick_id, 1);
				&regist_you_data($cs{$k}[$i], $kc, int($datas{$kc} * 0.5));
				
				$cs{$k}[$i] = '';
				$cs{$kc}[$i] = 0;
				
			}
		}
	}
	
	if ($w{year} % $reset_ceo_cycle_year == 0) {
		&write_world_news("<b>各国の$e2j{ceo}の任期が満了となりました</b>");
	}
	if ($w{year} % $reset_daihyo_cycle_year == 0) {
		&write_world_news("<b>各国の代表\者の任期が満了となりました</b>");
	}

	# 特殊情勢開始処理
	if (&is_special_world) { # 特殊情勢開始
		if ($w{year} =~ /6$/) { # 暗黒・英雄開始
			if ($w{year} =~ /06$/ || $w{year} =~ /26$/ || $w{year} =~ /46$/ || $w{year} =~ /66$/ || $w{year} =~ /86$/) { # 英雄開始
				$w{world} = $#world_states-4;
				$w{game_lv} += 20;
				for my $i (1 .. $w{country}) {
					$cs{strong}[$i]     = int(rand(15) + 25) * 1000;
				}
			}
			else { # 暗黒開始
				require './lib/vs_npc.cgi';
				&add_npc_country;
			}
		}
		else { # 祭り情勢開始
			require './lib/_festival_world.cgi';
			my $migrate_type = &opening_festival;
#			if ($w{year} % 40 == 0){ # 不倶戴天
#				$migrate_type = &festival_type('kouhaku', 1);
#				$w{world} = $#world_states-2;
#			} elsif ($w{year} % 40 == 20) { # 三国志
#				$migrate_type = &festival_type('sangokusi', 1);
#				$w{world} = $#world_states-3;
#			} elsif ($w{year} % 40 == 10) { # 拙速
#				$migrate_type = &festival_type('sessoku', 1);
#				$w{world} = $#world_states-5;
#			} else { # 混乱
#				$migrate_type = &festival_type('konran', 1);
#				$w{world} = $#world_states-1;
#			}
			&wt_c_reset;
#			if ($w{world} eq $#world_states-1) { # 混乱
#			}
#			elsif ($w{world} eq $#world_states-2) { # 不倶戴天
#				$migrate_type = &festival_type('kouhaku', 0);
#				$w{country} -= 2;
#			}
#			elsif ($w{world} eq $#world_states-3) { # 三国志
#				$w{country} -= 3;
#			}
#			elsif ($w{world} eq $#world_states-5) { # 拙速
#			}
			&player_migrate($migrate_type);
		}
#		$w{world} = int(rand($#world_states-5));
	}
	else {
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
		$w{game_lv} = $w{world} eq '15' || $w{world} eq '17' ? int($w{game_lv} * 0.7):$w{game_lv};
	}

	# 世界情勢 暗黒突入
#	if ($w{year} =~ /6$/) {
#		if ($w{year} =~ /06$/ || $w{year} =~ /26$/ || $w{year} =~ /46$/ || $w{year} =~ /66$/ || $w{year} =~ /86$/) { # 英雄
#			$w{world} = $#world_states-4;
#			$w{game_lv} += 20;
#			for my $i (1 .. $w{country}) {
#				$cs{strong}[$i]     = int(rand(15) + 25) * 1000;
#			}
#		} else {
#			require './lib/vs_npc.cgi';
#			&add_npc_country;
#		}
#	}
#	# 世界情勢 混乱突入
#	if ($w{year} =~ /0$/) {
#		require './lib/_festival_world.cgi';
#		if ($w{year} % 40 == 0){ # 不倶戴天
#			$w{world} = $#world_states-2;
#		} elsif ($w{year} % 40 == 20) { # 三国志
#			$w{world} = $#world_states-3;
#		} elsif ($w{year} % 40 == 10) { # 拙速
#			$w{world} = $#world_states-5;
#		} else { # 混乱
#			$w{world} = $#world_states-1;
#		}
#		&wt_c_reset;
#	}
	
	# 1000年デフォルト
	if ($w{year} =~ /000$/) {
		for my $i (1 .. $w{country}) {
			$cs{win_c}[$i] = 0;
		}
	}

	&write_cs;
#	return $migrate_type;
}

1; # 削除不可
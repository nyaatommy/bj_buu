#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
require "./lib/move_player.cgi";
my $this_script = 'admin_country.cgi';
#=================================================
# 国データ作成/追加/復元 Created by Merino
#=================================================

# おまかせで出力されるデータ
# ※NPCを細かく設定したい場合は、作成された「./data/npc_war_国No.cgi」をいじってね
my @countries = (qw/コルホーズ連邦 鎮国 百合桜国 五条 変態紳士教団 海底都市ﾙﾙｲｴ 賊国家パンドラ ｲｷﾞｽ連合 ｼﾚｼﾞｱ王国 ｱｸﾞｽﾄﾘｱ連合 ﾄﾗｷｱ王国 ｸﾞﾗﾝﾍﾞﾙ王国 ｲｻﾞｰｸ王国 ｳﾞｪﾙﾀﾞﾝ王国 ｵﾚﾝｼﾞ大国 ﾁｰｽﾞ連合 ｶﾅﾝ王国 ﾘｰｳﾞｪ王国 ﾚﾀﾞ王国 ｻﾘｱ王国/);
my @colors    = (qw/#006699 #0066CC #009999 #6600FF #0099CC #00CC99 #666699 #6699CC #3399CC #00CC00 #33CC33 #990000 #993333 #996633 #CC9966 #99CC66 #999999 #CC0000 #CC9900 #CC0099 #9900CC #CC3366/);
my @npcs = (
	['ｱﾙｳﾞｨｽ皇帝(NPC)',	'ｽﾌｧｰﾙ軍師(NPC)',	'ｾﾘｽ将軍(NPC)',		'ｸﾙﾄ将軍(NPC)',		'ｱｰﾀﾞﾝ隊長(NPC)'],
	['ﾉﾃﾞｨｵﾝ卿(NPC)',	'ｼｬｶﾞｰﾙ軍師(NPC)',	'ｴﾙﾄｼｬﾝ将軍(NPC)',	'ｲｰｳﾞ将軍(NPC)',	'ﾄﾙｰﾄﾞ隊長(NPC)'],
	['ｱﾘｵｰﾝ皇帝(NPC)',	'ｱｳｸﾞｽﾄ軍師(NPC)',	'ｲﾘｵｽ将軍(NPC)',	'ﾐﾝﾂ将軍(NPC)',		'ｱﾙﾊﾞ隊長(NPC)'],
	['ｾｲﾚｰﾝ皇女(NPC)',	'ｾﾃｨ軍師(NPC)',		'ﾗﾝﾃﾞｨｳｽ将軍(NPC)',	'ﾘｰｳﾞｧｽ将軍(NPC)',	'ｱﾐｯﾄﾞ隊長(NPC)'],
	['ｱﾘｵｰﾝ皇帝(NPC)',	'ｱｳｸﾞｽﾄ軍師(NPC)',	'ｲﾘｵｽ将軍(NPC)',	'ﾐﾝﾂ将軍(NPC)',		'ｱﾙﾊﾞ隊長(NPC)'],
	['ﾊﾞﾛﾝ伯爵(NPC)',	'ｱﾙﾄ軍師(NPC)',		'ﾗﾝﾌｫｰﾄﾞ将軍(NPC)',	'ﾀﾞﾅﾝ将軍(NPC)',	'ﾊﾞﾙﾄﾞ隊長(NPC)'],
	['ｸﾚｵﾊﾟﾄﾗ皇女(NPC)','ﾏｯｸｽ軍師(NPC)',	'ｻﾑ将軍(NPC)',		'ﾐｽﾃｨｰ将軍(NPC)',	'ﾐｰ隊長(NPC)'],
	['ｽｰﾃｨ皇子(NPC)',	'ﾃｨｶﾞｰ軍師(NPC)',	'ﾙｰｼｰ将軍(NPC)',	'ｽﾓｰｷｰ将軍(NPC)',	'ﾁｬｰﾘｰ隊長(NPC)'],
	['ｼﾞｪｲｸ閣下(NPC)',	'ｼﾞｬｯｸ軍師(NPC)',	'ｼﾞｮﾙｼﾞｪ将軍(NPC)',	'ｼﾞｪﾆｰ将軍(NPC)',	'ｼﾞｮﾝ隊長(NPC)'],
	['ﾄﾘｸｼｰ卿(NPC)',	'ﾎﾟﾘｰ軍師(NPC)',	'ﾚﾃﾞｨ将軍(NPC)',	'ﾒﾘｰ将軍(NPC)',		'ﾓﾘｰ隊長(NPC)'],
	['ｼﾞｪｲｺﾌﾞ皇王(NPC)','ﾏｼｭｰ軍師(NPC)',	'ｼﾞｮｼｭｱ将軍(NPC)',	'ﾏｲｹﾙ将軍(NPC)',	'ｲｰｻﾝ隊長(NPC)'],
	['ｴﾐﾘｰ皇女(NPC)',	'ｴﾏ軍師(NPC)',		'ﾏﾃﾞｨｿﾝ将軍(NPC)',	'ｵﾘﾋﾞｱ将軍(NPC)',	'ﾊﾝﾅ隊長(NPC)'],
	['ﾊﾞｼﾞﾙ皇帝(NPC)',	'ﾏｰﾁ軍師(NPC)',		'ﾊﾞﾆﾗ将軍(NPC)',	'ｶﾙﾋﾞｰ将軍(NPC)',	'ﾎﾟｯｷｰ隊長(NPC)'],
);
my %npc_statuss = (
	max_hp => [999, 500, 250, 150, 100],
	max_mp => [999, 300, 100, 100, 50],
	at     => [700, 400, 200, 100, 50],
	df     => [500, 300, 200, 100, 50],
	mat    => [700, 400, 200, 100, 50],
	mdf    => [500, 300, 200, 100, 50],
	ag     => [800, 500, 200, 100, 50],
	cha    => [800, 500, 200, 100, 50],
	lea    => [500, 350, 150, 80,  40],
	rank   => [$#ranks, $#ranks-2, 8, 5, 3],
);
my @npc_weas = (
#	[0]属性[1]武器No	[2]必殺技
	['無', [0],			[61..65],],
	['剣', [1 .. 5],	[1 .. 5],],
	['槍', [6 ..10],	[11..15],],
	['斧', [11..15],	[21..25],],
	['炎', [16..20],	[31..35],],
	['風', [21..25],	[41..45],],
	['雷', [26..30],	[51..55],],
	['銃', [34],			[71..75],],
);


#=================================================
# メイン処理
#=================================================
&header;
&decode;
&error('ﾊﾟｽﾜｰﾄﾞが違います') unless $in{pass} eq $admin_pass;
&header_admin;

if    ($in{mode} eq 'now_country')     { &now_country;     }
elsif ($in{mode} eq 'add_country')     { &admin_add_country;     }
elsif ($in{mode} eq 'delete_country')  { &admin_delete_country;  }
elsif ($in{mode} eq 'restore_country') { &restore_country; }
elsif ($in{mode} eq 'modify_country') { &modify_country; }
elsif ($in{mode} eq 'change_year')     { &admin_change_year;     }
elsif ($in{mode} eq 'change_game_lv')     { &admin_change_game_lv;     }
elsif ($in{mode} eq 'change_world')     { &admin_change_world;     }
elsif ($in{step}) { &{ 'step_' . $in{step} }; }
else { &step_1; }
&footer;
exit;



#=================================================
# header+
#=================================================
sub header_admin {
	print <<"EOM";
	<table border="0"><tr><td>
		<form action="$script_index">
			<input type="submit" value="ＴＯＰ" class="button1">
		</form>
	</td><td>
		<form method="$method" action="admin.cgi">
			<input type="hidden" name="pass" value="$in{pass}">
			<input type="submit" value="ﾌﾟﾚｲﾔｰ管理" class="button1">
		</form>
	</td><td>
		<form method="$method" action="$this_script">
			<input type="hidden" name="pass" value="$in{pass}">
			<input type="submit" value="国管理" class="button1">
		</form>
	</td><td>
		<form method="$method" action="$this_script">
			<input type="hidden" name="mode" value="now_country">
			<input type="hidden" name="pass" value="$in{pass}">
			<input type="submit" value="現在の国データ" class="button1">
		</form>
	</td></tr></table>
EOM
}


#=================================================
# 現在の国データ
#=================================================
sub now_country {
print qq|<p>現在の国データ</p>|;
	&read_cs;
	&countries_html;
}


#=================================================
# Step1
#=================================================
sub step_1 {
	print <<"EOM";
	<br>
	<div class="mes">
		<ul>
			<li>世界の国の数と始まりの年と情勢を入力してください。
			<li>国を途中で増やしたり減らしたりすることは可能\です。
			<li>特にこだわりがない場合はﾃﾞﾌｫﾙﾄのままでOKです。
			<li>国の数は１国からいくらでも増やすことが可能\です。
			<li>国の数により難易度が変わってくるので、極端に多い/少ない場合は ./lib/reset.cgi で難易度設定を変えることを推奨します。
		</ul>
	</div>
	<br>
	<form method="$method" action="$this_script">
		<input type="text" name="country" value="6" class="text_box_s" style="text-align: right">国<br>
		<input type="text" name="year"    value="1" class="text_box_s" style="text-align: right">年<br>
		<select name="world">
EOM
		for my $i (0 .. $#world_states) {
			my $selected = $in{world} == $i ? " selected=\"selected\"" : "";
			print qq|<option value="$i" label="$world_states[$i]"$selected>$world_states[$i]</option>|;
		}
	print <<"EOM";
		</select>情勢<br>
		<input type="hidden" name="step" value="2">
		<input type="hidden" name="pass" value="$in{pass}">
		<p><input type="submit" value="決定" class="button_s"></p>
	</form>
EOM
	if (-s "$logdir/countries.cgi") {
		print <<"EOM";
	<br><br><hr>
	<br>
	<div class="mes">
	年を変更する<br>
	<form method="$method" action="$this_script">
		<input type="hidden" name="mode" value="change_year">
		<input type="hidden" name="pass" value="$in{pass}">
		<input type="text" name="year" value="1" class="text_box_s" style="text-align: right">年<br>
		<p><input type="submit" value="変更" class="button1"></p>
	</form>
	</div>
	<br>
	<div class="mes">
	統一難易度を変更する<br>
	<form method="$method" action="$this_script">
		<input type="hidden" name="mode" value="change_game_lv">
		<input type="hidden" name="pass" value="$in{pass}">
		<input type="text" name="game_lv" value="1" class="text_box_s" style="text-align: right">Lv<br>
		<p><input type="submit" value="変更" class="button1"></p>
	</form>
	</div>
	<br>
	<div class="mes">
	情勢を変更する<br>
	<form method="$method" action="$this_script">
		<input type="hidden" name="mode" value="change_world">
		<input type="hidden" name="pass" value="$in{pass}">
		<select name="world">
EOM
		for my $i (0 .. $#world_states) {
			my $selected = $in{world} == $i ? " selected=\"selected\"" : "";
			print qq|<option value="$i" label="$world_states[$i]"$selected>$world_states[$i]</option>|;
		}
	print <<"EOM";
		</select>情勢<br>
		<p><input type="submit" value="変更" class="button1"></p>
	</form>
	</div>
	<br>
	<div class="mes">
	国を追加する<br>
	<form method="$method" action="$this_script">
		<input type="hidden" name="mode" value="add_country">
		<input type="hidden" name="pass" value="$in{pass}">
		国名：<input type="text" name="add_name"  class="text_box1"><br>
		国色：<input type="text" name="add_color" class="text_box1"><br>
		<p><input type="submit" value="追加" class="button1"></p>
	</form>
	</div>
	<br>
	<div class="mes">
	国を削除(一番後ろの国からしか削除できません)<br>
	<form method="$method" action="$this_script">
		<input type="hidden" name="mode" value="delete_country">
		<input type="hidden" name="pass" value="$in{pass}">
		<p><input type="submit" value="削除" class="button1"></p>
	</form>
	</div>
	<br>
	<div class="mes">
	国を修正<br>
	<form method="$method" action="$this_script">
		<input type="hidden" name="mode" value="modify_country">
		<input type="hidden" name="pass" value="$in{pass}">
		<p><input type="submit" value="修正" class="button1"></p>
	</form>
	</div>
	<br>
EOM
	}
	
	&backup if $is_backup_countries && -d "backup";
}
#=================================================
# Step2
#=================================================
sub step_2 {
	print <<"EOM";
	<p>全$in{country}カ国。$in{year}年目の$world_states[$in{world}]から始まり</p>
	<p>国の名前と色を決めてください</p>
	<form method="$method" action="$this_script">
		<input type="hidden" name="year" value="$in{year}">
		<input type="hidden" name="world" value="$in{world}">
		<input type="hidden" name="step" value="2">
		<input type="hidden" name="country" value="$in{country}">
		<input type="hidden" name="omakase" value="1">
		<input type="hidden" name="pass" value="$in{pass}">
		<input type="submit" value="おまかせ" class="button1">
	</form>
	<form method="$method" action="$this_script">
EOM
	for my $i (1 .. $in{country}) {
		my $country = '';
		my $color   = '';
		
		if ( $in{omakase} && defined($countries[0]) && defined($colors[0]) ) {
			my $v  = int(rand(@countries));
			my $vv = int(rand(@colors));
			$country = splice(@countries, $v, 1);
			$color   = splice(@colors, $vv, 1);
		}

		print qq|国の名前： <input type="text" name="name_$i" class="text_box1" value="$country">|;
		print qq|　国の色： <input type="text" name="color_$i" class="text_box1" value="$color" style="color: #333; background-color: $color;"><br>|;
	}
	
	print <<"EOM";
		<input type="hidden" name="year" value="$in{year}">
		<input type="hidden" name="world" value="$in{world}">
		<input type="hidden" name="country" value="$in{country}">
		<input type="hidden" name="pass" value="$in{pass}">
		<input type="hidden" name="step" value="3">
		<p><input type="submit" value="決定" class="button_s"></p>
	</form>
EOM
}
#=================================================
# Step3
#=================================================
sub step_3 {
	%w = ();
	%cs = ();
	
	$in{year} = 1 if $in{year} < 0;
	--$in{year};
print "$w{country}<br>" if $config_test;
	
	$w{country} = $in{country};
print "$w{country}<br>" if $config_test;
	$w{year}    = $in{year};
	$w{world}   = $in{world};
	$w{playing} = 0;

	for my $i (1 .. $in{country}) {
		&error('名前か色が未記入の国があります') if !$in{"name_$i"} || !$in{"color_$i"};
		
		$cs{name}[$i]     = $in{"name_$i"};
		$cs{color}[$i]    = $in{"color_$i"};
		$cs{member}[$i]   = 0;
		$cs{win_c}[$i]    = 0;
		$cs{tax}[$i]      = 30;
		
		# ﾌｧｲﾙなど作成
		mkdir "$logdir/$i" or &error("$logdir/$i ﾌｫﾙﾀﾞが作れませんでした") unless -d "$logdir/$i";
		for my $file_name (qw/bbs bbs_log bbs_member depot_log depot_b depot_b_log leader member patrol prison prison_member prisoner violator/) {
			my $output_file = "$logdir/$i/$file_name.cgi";
#			next if -f $output_file;
			open my $fh, "> $output_file" or &error("$output_file ﾌｧｲﾙが作れませんでした");
			close $fh;
			chmod $chmod, $output_file;
		}
		for my $file_name (1 .. $in{country}) {
			if ($file_name != $i) {
				my $output_file = "$logdir/$i/bbs_log_$file_name.cgi";
				open my $fh, "> $output_file" or &error("$output_file ﾌｧｲﾙが作れませんでした");
				close $fh;
				chmod $chmod, $output_file;
			}
		}
		# 国庫は1行目が設定なので予め書き込んでおかないと国庫にぶち込んだ1個目のアイテムが消失してしまう
		my $output_file = "$logdir/$i/depot.cgi";
		open my $fh, "> $output_file" or &error("$output_file ﾌｧｲﾙが作れませんでした");
		print $fh "1<>1<>1世代Lv1以上が利用できます<>\n";
		close $fh;
		chmod $chmod, $output_file;
		
		&add_npc_data($i);
		
		mkdir "$logdir/union" or &error("$logdir/union ﾌｫﾙﾀﾞが作れませんでした") unless -d "$logdir/union";
		
		# create union file
		for my $j ($i+1 .. $in{country}) {
			my $file_name = "$logdir/union/${i}_${j}";
#			next if -f "$file_name.cgi";
			open my $fh, "> $file_name.cgi" or &error("$file_name.cgi ﾌｧｲﾙが作れません");
			close $fh;
			chmod $chmod, "$file_name.cgi";
			
			open my $fh2, "> ${file_name}_log.cgi" or &error("${file_name}_log.cgi ﾌｧｲﾙが作れません");
			close $fh2;
			chmod $chmod, "${file_name}_log.cgi";
			
			open my $fh3, "> ${file_name}_member.cgi" or &error("${file_name}_member.cgi ﾌｧｲﾙが作れません");
			close $fh3;
			chmod $chmod, "${file_name}_member.cgi";
		}
		
		open my $fh_h, "> $htmldir/$i.html" or &error("$htmldir/$i.html ﾌｧｲﾙが作れません");
		close $fh_h;
	}
	
	$w{player} = 0;
	opendir my $dh, "$userdir" or &error('ﾕｰｻﾞｰﾌｫﾙﾀﾞが開けません');
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /\./;
		next if $file_name =~ /backup/;
		++$w{player};
	}
	closedir $dh;
	
	require './lib/reset.cgi';
	&reset;
	&begin_common_world;

	&write_cs;
	&create_countries_mes;

	print qq|<p>以下のような国データを作成しました!</p>|;
	&countries_html;
}


#=================================================
# 国一覧表示
#=================================================
sub countries_html {
	print qq|<table class="table1">|;

	print qq|<tr><th>$e2j{name}</th>|;
	print qq|<td align="center" style="color: #333; background-color: $cs{color}[$_];">$cs{name}[$_]</td>| for (1 .. $w{country});
	print qq|</tr>\n|;

	for my $k (qw/strong food money soldier tax/) {
		print qq|<tr><th>$e2j{$k}</th>|;
		for my $i (1 .. $w{country}) {
			print qq|<td align="right">$cs{$k}[$i]</td>|;
		}
		print qq|</tr>\n|;
	}

	print qq|<tr><th>$e2j{state}</th>|;
	print qq|<td align="center">$country_states[ $cs{state}[$_] ]</td>| for (1 .. $w{country});
	print qq|</tr>\n|;

	print qq|</table>|;
}


#=================================================
# NPCを作成
#=================================================
sub add_npc_data {
	my $country = shift;
	my $v     = int(rand(@npcs));
	my $names = splice(@npcs, $v, 1);
	my @names = @{ $names };
	
	my $line = qq|\@npcs = (\n|;
	
	for my $i (0..4) {
		$line .= qq|\t{\n\t\tname\t\t=> '$names[$i]',\n|;
		
		for my $k (qw/max_hp max_mp at df mat mdf ag cha lea rank/) {
			$line .= qq|\t\t$k\t\t=> $npc_statuss{$k}[$i],\n|;
		}
		
		my $kind = int(rand(@npc_weas));
		my @weas = @{ $npc_weas[$kind][1] };
		my $wea  = $npc_weas[$kind][1]->[int(rand(@weas))];
		$line .= qq|\t\twea\t\t=> $wea,\n|;

		my $skills = join ',', @{ $npc_weas[$kind][2] };
		$line .= qq|\t\tskills\t\t=> '$skills',\n\t},\n|;
	}
	
	$line .= qq|);\n\n1;\n|;
	
	open my $fh, "> $datadir/npc_war_$country.cgi";
	print $fh $line;
	close $fh;
}

#=================================================
# 国の方針ﾌｧｲﾙ作成
#=================================================
sub create_countries_mes {
	open my $fh, "> $logdir/countries_mes.cgi";
	for my $i (0 .. $in{country}) {
		print $fh "<><>\n";
	}
	close $fh;
}

#=================================================
# 年を変更
#=================================================
sub admin_change_year {
	&read_cs;
	$w{year} = $in{year}-1;
	&write_cs;

	require "./lib/reset.cgi";
	&reset;

	print qq|<p>以下のような国データで年を$w{year}にしました!</p>|;
	&countries_html;
}

#=================================================
# 統一難易度を変更
#=================================================
sub admin_change_game_lv {
	&read_cs;
	$w{game_lv} = $in{game_lv};
	&write_cs;

	print qq|<p>統一難易度を$w{game_lv}にしました!</p>|;
}

#=================================================
# 情勢を変更
#=================================================
sub admin_change_world {
	&read_cs;
	$w{world} = $in{world};
	&write_cs;

	print qq|<p>情勢を$w{world}にしました!</p>|;
}


#=================================================
# 国を追加
#=================================================
sub admin_add_country {
	&read_cs;
	&error('名前か色が未記入です') if !$in{"add_name"} || !$in{"add_color"};

	++$w{country};
	
	my $i = $w{country};

	# ﾌｧｲﾙなど作成してしまう
	mkdir "$logdir/$i" or &error("$logdir/$i ﾌｫﾙﾀﾞが作れませんでした") unless -d "$logdir/$i";
	for my $file_name (qw/bbs bbs_log bbs_member depot depot_log leader member patrol prison prison_member prisoner violator/) {
		my $output_file = "$logdir/$i/$file_name.cgi";
#		next if -f $output_file;
		open my $fh, "> $output_file" or &error("$output_file ﾌｧｲﾙが作れませんでした");
		close $fh;
		chmod $chmod, $output_file;
	}
	
	&add_npc_data($i);
	
	# create union file
	for my $j (1 .. $i-1) {
		my $file_name = "$logdir/union/${j}_${i}";
#		next if -f "$file_name.cgi";
		open my $fh, "> $file_name.cgi" or &error("$file_name.cgi ﾌｧｲﾙが作れません");
		close $fh;
		chmod $chmod, "$file_name.cgi";
		
		open my $fh2, "> ${file_name}_log.cgi" or &error("${file_name}_log.cgi ﾌｧｲﾙが作れません");
		close $fh2;
		chmod $chmod, "${file_name}_log.cgi";
		
		open my $fh3, "> ${file_name}_member.cgi" or &error("${file_name}_member.cgi ﾌｧｲﾙが作れません");
		close $fh3;
		chmod $chmod, "${file_name}_member.cgi";

		$w{ "f_${j}_${i}" } = int(rand(50)+10);
		$w{ "p_${j}_${i}" } = 0;
	}
	
	open my $fh_h, "> $htmldir/$i.html" or &error("$htmldir/$i.html ﾌｧｲﾙが作れません");
	print $fh_h "準備中…$date 次の日に何度かログインすると更新されます";
	close $fh_h;
	my $country = $w{world} eq $#world_states ? $w{country} - 1 : $w{country};
	my $ave_c = int($w{player} / $country);
	$cs{name}[$i]     = $in{"add_name"};
	$cs{color}[$i]    = $in{"add_color"};
	$cs{member}[$i]   = 0;
	$cs{win_c}[$i]    = 0;
	$cs{tax}[$i]      = 30;
	$cs{strong}[$i]   = int(rand(6)  + 7) * 1000;
	$cs{food}[$i]     = int(rand(10) + 3) * 1000;
	$cs{money}[$i]    = int(rand(10) + 3) * 1000;
	$cs{soldier}[$i]  = int(rand(10) + 3) * 1000;
	$cs{state}[$i]    = rand(2) > 1 ? 0 : int(rand(@country_states));
	$cs{capacity}[$i] = $ave_c;
	$cs{is_die}[$i]   = 0;
	
	&write_cs;
	
	open my $fh9, ">> $logdir/countries_mes.cgi";
	print $fh9 "<><>\n";
	close $fh9;
	
	print qq|<p>国を追加しました</p>|;
	&countries_html;
}

#=================================================
# 国を復元
#=================================================
sub restore_country {
	my @lines = ();
	open my $fh, "< ./backup/$in{file_name}" or &error("./backup/$in{file_name}ﾌｧｲﾙが読み込めません");
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	close $fh;
	
	open my $fh2, "> $logdir/countries.cgi" or &error("$logdir/countries.cgiﾌｧｲﾙが開けません");
	print $fh2 @lines;
	close $fh2;
	
	print qq|<p>国ﾃﾞｰﾀを復元しました</p>|;
	
	&read_cs;
	&countries_html;
}

#=================================================
# 国を削除
#=================================================
sub admin_delete_country {
	&read_cs;
	
	my @lines = &get_country_members($w{country});
	for my $line (@lines) {
		$line =~ tr/\x0D\x0A//d;
		&move_player($line, $w{country}, 0);
		&regist_you_data($line, 'country', 0);
	}
	--$w{country};
	&write_cs;
	
	print qq|<p>$cs{name}[$w{country}+1]を削除しました</p>|;
	&countries_html;
}


#=================================================
# ﾊﾞｯｸｱｯﾌﾟﾌｫｰﾑ
#=================================================
sub backup {
	my %files = ();
	opendir my $dh, "backup" or &error("backupﾌｫﾙﾀﾞが開けません");
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		next if $file_name =~ /index.html/;
		
		my $file_time = (stat "./backup/$file_name")[9];
		$files{$file_time} = $file_name;
	}
	closedir $dh;

	print qq|<form method="$method" action="$this_script">|;
	print qq|<div class="mes">ﾊﾞｯｸｱｯﾌﾟから復元<br>|;
	print qq|<select name="file_name" class="select1">|;
	
	for my $k (sort { $b <=> $a } keys %files) {
		my($hour, $day, $month) = (localtime($k))[2,3,4];
		++$month;
		print qq|<option value="$files{$k}">$month月$day日$hour:00</option>|;
	}
	print qq|</select><br>|;
	print qq|<input type="hidden" name="pass" value="$in{pass}"><input type="hidden" name="mode" value="restore_country">|;
	print qq|<p><input type="submit" value="復元" class="button1"></p></form></div>|;
}

#=================================================
# 修正
#=================================================
sub modify_country {
	&read_cs;

	if ($in{execute}) {
		for my $i (1..$w{country}) {
			$cs{color}[$i] = $in{"color_" . $i};
			$cs{name}[$i] = $in{"name_" . $i};
			for my $k (qw/strong food money soldier tax state is_die modify_war modify_dom modify_mil modify_pro/) {
				$cs{$k}[$i] = $in{$k . "_" . $i};
				if ($cs{$k}[$i] =~ /[^0-9]/ || $cs{$k}[$i] < 0) {
					$cs{$k}[$i] = 0;
				}
			}
		}
		&write_cs;
	}
	
	print <<"EOM";
	<p>国の情報を決めてください</p>
	<form method="$method" action="$this_script">
		<input type="hidden" name="mode" value="modify_country">
		<input type="hidden" name="execute" value="1">
		<input type="hidden" name="pass" value="$in{pass}">
EOM
	print qq|<table class="table1">|;

	print qq|<tr><th>色</th>|;
	for my $i (1 .. $w{country}) {
		print qq|<td align="center" style="color: #333; background-color: $cs{color}[$i];"><input type="text" name="color_${i}" value="$cs{color}[$i]"/></td>|;
	}
	print qq|</tr>\n|;

	print qq|<tr><th>$e2j{name}</th>|;
	for my $i (1 .. $w{country}) {
		print qq|<td align="center" style="color: #333; background-color: $cs{color}[$i];"><input type="text" name="name_${i}" value="$cs{name}[$i]"/></td>|;
	}
	print qq|</tr>\n|;

	for my $k (qw/strong food money soldier tax/) {
		print qq|<tr><th>$e2j{$k}</th>|;
		for my $i (1 .. $w{country}) {
			print qq|<td align="right"><input type="text" name="${k}_${i}" value="$cs{$k}[$i]"/></td>|;
		}
		print qq|</tr>\n|;
	}

	print qq|<tr><th>$e2j{state}</th>|;
	for my $i (1 .. $w{country}) {
		print qq|<td align="right">|;
		print qq|<select name="state_${i}">|;
		for my $j (0..$#country_states) {
			my $selected = $cs{state}[$i] eq $j ? ' selected' : '';
			print qq|<option value="$j"$selected>$country_states[$j]</option>|;
		}
		print qq|</select>|;
		print qq|</td>|;
	}
	print qq|</tr>\n|;

	print qq|<tr><th>滅亡</th>|;
	for my $i (1 .. $w{country}) {
		print qq|<td align="right">|;
		print qq|<select name="is_die_${i}">|;
		my $selected = $cs{is_die}[$i] eq 1 ? ' selected' : '';
		print qq|<option value="0"$selected>復興</option>|;
		print qq|<option value="1"$selected>滅亡</option>|;
		print qq|</select>|;
		print qq|</td>|;
	}
	print qq|</tr>\n|;

	for my $k (qw/modify_war modify_dom modify_mil modify_pro/) {
		print qq|<tr><th>$k</th>|;
		for my $i (1 .. $w{country}) {
			print qq|<td align="right"><input type="text" name="${k}_${i}" value="$cs{$k}[$i]"/></td>|;
		}
		print qq|</tr>\n|;
	}

	print qq|</table>|;	
	print <<"EOM";
		<p><input type="submit" value="修正" class="button_s"></p>
	</form>
EOM
}


#================================================
# toto
#================================================
require './lib/_comment_tag.cgi';
require './lib/_casino_funcs.cgi';

# 賭け情報
my $bet_file = "$logdir/toto.cgi";

# 1票当たりの金額
my $rate = 10000;

# 開催に必要なｺｲﾝ（票）
my $make_fee = 100;

# 控除率
my $house_edge = 0.05;
my $house_edge_dark = 0.25;

# 賭けの種類
my @kinds = (
	['strong', '奪国力'],
	['nou', '農業'],
	['sho', '商業'],
	['hei', '徴兵'],
	['gou', '強奪'],
	['cho', '諜報'],
	['sen', '洗脳'],
	['gik', '偽計'],
	['res', '救出'],
	['esc', '脱獄'],
	['tei', '偵察'],
	['stop', '停戦'],
	['pro', '友好'],
	['dai', '国畜'],
);

unless (-f $bet_file) {
	open my $fh, "> $bet_file" or &error('賭けﾌｧｲﾙの書き込みに失敗しました');
	print $fh "<><><>\n";
	close $fh;
}

my $wc = $w{world} eq $#world_states ? $w{country} - 1 : $w{country};

sub run {
	if ($in{mode} eq "make_game") {
		$in{comment} = &make_game;
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "bet") {
		&bet;
	}
	elsif($in{mode} eq "write" &&$in{comment}){
		&write_comment;
	}
	my ($member_c, $member) = &get_member;

	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="戻る" class="button1"></form>|;
	print qq|<h2>$this_title</h2>|;
	
	if (&isPlaying) {
		my ($leadar, $year, $odds) = &get_toto_data;
		print qq|$year年$leadar杯<br>|;
		print qq|<hr>|;
		print qq|現在のオッズ<br>$odds|;
		print qq|<hr>|;
		print qq|1口 $rate ｺｲﾝ<br>|;
		print qq|<form method="$method" action="$this_script">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="hidden" name="mode" value="bet">|;
		print qq|<input type="text" name="bet" value="1">|;
		print qq|<select name="bet_country">|;
		print qq|<option value=""></option>|;
		for my $c (1..$wc) {
			print qq|<option value="$c">$cs{name}[$c]</option>|;
		}
		print qq|</select>|;
		print qq|<input type="submit" value="賭ける" class="button1"></form>|;
	} elsif (&isGaming) {
		my ($leadar, $year, $odds) = &get_toto_data;
		print qq|$year年$leadar杯<br>|;
		print qq|<hr>|;
		print qq|現在のオッズ<br>$odds|;
		print qq|<hr>|;
	} else {
		print qq|<form method="$method" action="$this_script">|;
		print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
		print qq|<input type="hidden" name="mode" value="make_game">|;
		print qq|<input type="submit" value="胴元になる" class="button1"></form>|;
	}
	print qq|<form method="$method" action="$this_script" name="form">|;
	print qq|<input type="text"  name="comment" class="text_box_b"><input type="hidden" name="mode" value="write">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="発言" class="button_s"><br>|;
	print qq|</form>|;

	print qq|<div id="body_mes"><font size="2">$member_c人:$member</font><br>|;
	
	print qq|<hr>|;

	open my $fh, "< $this_file.cgi" or &error("$this_file.cgi ﾌｧｲﾙが開けません");
	while (my $line = <$fh>) {
		my($btime,$bdate,$bname,$bcountry,$bshogo,$baddr,$bcomment,$bicon) = split /<>/, $line;
		$bname .= "[$bshogo]" if $bshogo;
		$bcomment = &comment_change($bcomment, 1);
		$is_mobile ? $bcomment =~ s|ハァト|<font color="#FFB6C1">&#63726;</font>|g : $bcomment =~ s|ハァト|<font color="#FFB6C1">&hearts;</font>|g;
		print qq|<font color="$cs{color}[$bcountry]">$bname：$bcomment <font size="1">($cs{name}[$bcountry] : $bdate)</font></font><hr size="1">\n|;
	}
	close $fh;
	print qq|</div>|;
	print qq|</td>|;
	print qq|</tr></table>|;
}
sub get_member {
	my $is_find = 0;
	my $member  = '';
	my @members = ();
	my %sames = ();
	
	open my $fh, "+< ${this_file}_member.cgi" or &error('ﾒﾝﾊﾞｰﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		my($mtime, $mname, $maddr) = split /<>/, $line;
		next if $time - $limit_member_time > $mtime;
		next if $sames{$mname}++; # 同じ人なら次
		
		if ($mname eq $m{name}) {
			push @members, "$time<>$m{name}<>$addr<>\n";
			$is_find = 1;
		}
		else {
			push @members, $line;
		}
		$member .= "$mname,";
	}
	unless ($is_find) {
		push @members, "$time<>$m{name}<>$addr<>\n";
		$member .= "$m{name},";
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	my $member_c = @members;

	return ($member_c, $member);
}

sub isPlaying {
	open my $fh, "< $bet_file" or &error('賭けﾌｧｲﾙが開けません'); 
	my $headline = <$fh>;
	my($leadar, $year, $kind) = split /<>/, $headline;
	close $fh;
	return ($year == $w{year} + 1);
}

sub isGaming {
	open my $fh, "< $bet_file" or &error('賭けﾌｧｲﾙが開けません'); 
	my $headline = <$fh>;
	my($leadar, $year, $kind) = split /<>/, $headline;
	close $fh;
	return ($year == $w{year});
}

sub make_game {
	my $mmes = '';
	my @members = ();
	
	if ($m{coin} < $make_fee * $rate) {
		return "親になるには$make_fee票分のｺｲﾝが必要です。";
	}
	if ($m{year} =~ /[59]$/) {
		return "祭り情勢の開催はできません。";
	}
	
	open my $fh, "+< $bet_file" or &error('賭けﾌｧｲﾙが開けません'); 
	eval { flock $fh, 2; };
	my $headline = <$fh>;
	my($leadar, $year, $kind) = split /<>/, $headline;
	if ($year < $w{year}) {
		$year = $w{year} + 1;
		$kind = int(rand(@kinds));
		push @members, "$m{name}<>$year<>$kind<>\n";
		push @members, "$m{name}<>-1<>$make_fee<>\n";
		$m{coin} -= $make_fee * $rate;
		$mmes .= "$year年$m{name}杯開催決定!投票募集中!";
		&write_user;
	} else {
		push @members, $headline;
		while (my $line = <$fh>) {
			push @members, $line;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @members;
	close $fh;

	return $mmes;
}

sub bet {
	if($in{bet_couontry} !~ /[^0-9]/ && $in{bet_country} > 0 && $in{bet_country} <= $w{country} && 
		$in{bet} > 0 && $in{bet} !~ /[^0-9]/ && $in{bet} * $rate < $m{coin}){
		my @members = ();

		open my $fh, "+< $bet_file" or &error('賭けﾌｧｲﾙが開けません'); 
		eval { flock $fh, 2; };
		my $headline = <$fh>;
		my($leadar, $year, $kind) = split /<>/, $headline;
		push @members, $headline;
		while (my $line = <$fh>) {
			push @members, $line;
			my($name, $country, $bet) = split /<>/, $line;
			if ($name eq $m{name} && $country != -1) {
				$in{bet_country} = $country;
			}
		}
		if ($year == $w{year} + 1) {
			push @members, "$m{name}<>$in{bet_country}<>$in{bet}<>\n";
			$m{coin} -= $in{bet} * $rate;
			&write_user;
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @members;
		close $fh;
	}
}

sub get_toto_data {
	my $odds = '';
	my @bets = ();
	my @my_bets = ();
	my $total_bets = 0;
	
	open my $fh, "< $bet_file" or &error('賭けﾌｧｲﾙが開けません'); 
	my $headline = <$fh>;
	my($leadar, $year, $kind) = split /<>/, $headline;
	while (my $line = <$fh>) {
		my($name, $country, $bet) = split /<>/, $line;
		if ($country != -1) {
			$bets[$country] += $bet;
			if ($name eq $m{name}) {
				$my_bets[$country] += $bet;
			}
		}
		$total_bets += $bet;
	}
	close $fh;
	
	for my $c (1..$wc) {
		my $cname = '';
		my $codds = 0;
		my $mbet = $my_bets[$c];
		$cname = $cs{name}[$c];
		my $bc = $bets[$c];
		if ($bc <= 0) {
			$bc = 1;
		}
		$codds = $total_bets * (1.0 - $house_edge - $house_edge_dark) / $bc;
		$odds .= "$cname : $codds 倍";
		if ($mbet) {
			$odds .= " $mbet 票投票中";
		}
		$odds .= "<br>";
	}
	
	return ($leadar, $year, $odds)
}

sub pay_back {
	my $pay_year = shift;
	
	my @bets = ();
	my $total_bets = 0;
	my $total_pay = 0;
	my %name_bet = ();
	
	open my $fh, "< $bet_file" or &error('賭けﾌｧｲﾙが開けません'); 
	my $headline = <$fh>;
	my($leadar, $year, $kind) = split /<>/, $headline;
	while (my $line = <$fh>) {
		my($name, $country, $bet) = split /<>/, $line;
		if ($country != -1) {
			$bets[$country] += $bet;
			if (!$name_bet{$name}) {
				$name_bet{$name} = ();
			}
			$name_bet{$name}[$country] += $bet;
		}
		$total_bets += $bet;
	}
	close $fh;
	
	if ($pay_year != $year) {
		return;
	}
	
	my $win_country = 0;
	
	my %sames = ();
	my $status = $kinds[$kind][0];
	my $max = 0.0;
	
	for my $country (0 .. $w{country}) {

		open my $cfh, "< $logdir/$country/member.cgi" or &error("$logdir/$country/member.cgiﾌｧｲﾙが開けません");

		while (my $player = <$cfh>) {
			$player =~ tr/\x0D\x0A//d;
			next if ++$sames{$player} > 1;
			my $player_id = unpack 'H*', $player;
			unless (-f "$userdir/$player_id/year_ranking.cgi") {
				next;
			}
			
			open my $fh, "< $userdir/$player_id/year_ranking.cgi" or &error("year_ranking.cgiﾌｧｲﾙが開けません");
			while (my $line = <$fh>) {
				my %ydata;
				for my $hash (split /<>/, $line) {
					my($k, $v) = split /;/, $hash;
					$ydata{$k} = $v;
					if($k eq 'year'){
						if($v != $pay_year){
							next;
						}
					}
				}
				if($ydata{year} == $pay_year){
					if($ydata{$status}){
						if ($max < $ydata{$status}) {
							$max = $ydata{$status};
							$win_country = $country;
						}
					}
				}
			}
			close $fh;
		}
		close $cfh;
	}
	
	my $world_mes = '賭け対象は ' . $kinds[$kind][1];
	$world_mes .= ' でした。当選国は ';
	my $bc = $bets[$win_country];
	$world_mes .= $cs{name}[$win_country] . 'で、';
	if ($bc <= 0) {
		$bc = 1;
	}
	my $odds = $total_bets * (1.0 - $house_edge - $house_edge_dark) / $bc;
	$world_mes .= '配当は' . $odds . '倍でした';
	for my $name (keys(%name_bet)) {
		my $get_coin = 0;
		if ($name_bet{$name}[$win_country] > 0) {
			$get_coin += int($name_bet{$name}[$win_country] * $odds * $rate);
		}
		if ($get_coin > 0) {
			$total_pay += $get_coin;
			&item_or_coin($get_coin, $name);
		}
	}
	
	&write_send_news(qq|<font color="#0000FF">$world_mes</font>|);
	&item_or_coin(int($total_bets * $house_edge), $leadar);
}

sub item_or_coin {
	my ($m_coin, $name) = @_;
	
	while ($m_coin > 2500000) {
		$m_coin -= 1000000;
		&bonus($name, '', 'ﾄﾄの景品を貰いました');
	}
	&coin_move($m_coin, $name, 1);
}

1;
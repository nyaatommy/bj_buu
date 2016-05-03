#================================================
# 限定じゃんけん
#================================================
require './lib/_comment_tag.cgi';
require './lib/_casino_funcs.cgi';

# 参加者一覧
my $all_member_file = "$logdir/espoir_member.cgi";

# ユーザーデータ
my $my_espoir_file = "$userdir/$id/espoir.cgi";

# 基準額
my $rate = 10;

my $overflow = 2500000;
my $bonus_coin = 2500000;

# 出港に必要な最低プレイヤー数
my $min_espoir = 3;

unless (-f $all_member_file) {
	open my $fh, "> $all_member_file" or &error('賭けﾌｧｲﾙの書き込みに失敗しました');
	print $fh "<>0<>0<>0<>\n";
	close $fh;
}

sub run {
	if ($in{mode} eq "participate") {
		$in{comment} = &participate;
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "send_star") {
		&send_star($in{to});
	}
	elsif ($in{mode} eq "send_a") {
		&send_a($in{to});
	}
	elsif ($in{mode} eq "send_b") {
		&send_b($in{to});
	}
	elsif ($in{mode} eq "send_c") {
		&send_c($in{to});
	}
	elsif ($in{mode} eq "receive") {
		&receive($in{type});
	}
	elsif ($in{mode} eq "refuse") {
		&refuse($in{type});
	}
	elsif ($in{mode} eq "check_a") {
		$in{comment} = &check_a($in{to});
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "check_b") {
		$in{comment} = &check_b($in{to});
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "check_c") {
		$in{comment} = &check_c($in{to});
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "recheck") {
		&recheck($in{hand});
	}
	elsif ($in{mode} eq "uncheck") {
		$in{comment} = &uncheck;
		&write_comment if $in{comment};
	}
	elsif ($in{mode} eq "goal") {
		&goal;
	}
	elsif($in{mode} eq "write" &&$in{comment}){
		&write_comment;
	}
	my ($member_c, $member) = &get_member;

	my ($game_year, $all_rest_a, $all_rest_b, $all_rest_c, $participate, @all_member) = &get_state;
	
	print qq|<form method="$method" action="$script">|;
	print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
	print qq|<input type="submit" value="戻る" class="button1"></form>|;
	print qq|<h2>$this_title</h2>|;
	
	if ($game_year eq $w{year}) {
		print qq|全体残り グー:$all_rest_a チョキ:$all_rest_b パー:$all_rest_c<br>|;
		if ($participate) {
			my ($rest_a, $rest_b, $rest_c, $star, $count, $year, $check_h, %stack) = &get_my_state;
			print qq|残り グー:$my_rest_a チョキ:$my_rest_b パー:$my_rest_c|;
			my $no_stack = 1;
			if (@{$stack{star}}) {
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="receive"><input type="hidden" name="type" value="1">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="${stack{star}}[0]からの星を受け取る" class="button_s"><br>|;
				print qq|</form>|;
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="refuse"><input type="hidden" name="type" value="1">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="${stack{star}}[0]からの星を受け取らない" class="button_s"><br>|;
				print qq|</form>|;
				$no_stack = 0;
			}
			if (@{$stack{a}}) {
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="receive"><input type="hidden" name="type" value="2">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="${stack{a}}[0]からのグーを受け取る" class="button_s"><br>|;
				print qq|</form>|;
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="refuse"><input type="hidden" name="type" value="2">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="${stack{a}}[0]からのグーを受け取らない" class="button_s"><br>|;
				print qq|</form>|;
				$no_stack = 0;
			}
			if (@{$stack{b}}) {
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="receive"><input type="hidden" name="type" value="3">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="${stack{b}}[0]からのチョキを受け取る" class="button_s"><br>|;
				print qq|</form>|;
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="refuse"><input type="hidden" name="type" value="3">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="${stack{b}}[0]からのチョキを受け取らない" class="button_s"><br>|;
				print qq|</form>|;
				$no_stack = 0;
			}
			if (@{$stack{c}}) {
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="receive"><input type="hidden" name="type" value="4">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="${stack{c}}[0]からのパーを受け取る" class="button_s"><br>|;
				print qq|</form>|;
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="refuse"><input type="hidden" name="type" value="4">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="${stack{c}}[0]からのパーを受け取らない" class="button_s"><br>|;
				print qq|</form>|;
				$no_stack = 0;
			}
			if (@{$stack{check}}) {
				if ($rest_a + $rest_b + $rest_c > 0) {
					print qq|<form method="$method" action="$this_script" name="form">|;
					print qq|<input type="hidden" name="mode" value="recheck">|;
					print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
					for my $i (1..3) {
						if (($i == 1 && $rest_a <= 0) || ($i == 2 && $rest_b <= 0) || ($i == 3 && $rest_c <= 0)) {
							next;
						}
						
						print qq|<input type="radio" name="hand" value="$i">|;
						print $i == 1 ? 'グー' :
								$i == 2 ? 'チョキ' :
										'パー';
					}
					print qq|<input type="submit" value="${stack{check}}[0]と勝負" class="button_s"><br>|;
					print qq|</form>|;
				}
				print qq|<form method="$method" action="$this_script" name="form">|;
				print qq|<input type="hidden" name="mode" value="uncheck">|;
				print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
				print qq|<input type="submit" value="${stack{check}}[0]と勝負しない" class="button_s"><br>|;
				print qq|</form>|;
				$no_stack = 0;
			}
			if (@{$stack{send}}) {
				$no_stack = 0;
			}
			if ($no_stack) {
				if ($rest_a + $rest_b + $rest_c > 0) {
					print qq|<form method="$method" action="$this_script" name="form">|;
					print qq|<select name="mode">|;
					if ($rest_a > 0) {
						print qq|<option value="check_a">グーで勝負</option>|;
					}
					if ($rest_b > 0) {
						print qq|<option value="check_b">チョキで勝負</option>|;
					}
					if ($rest_c > 0) {
						print qq|<option value="check_c">パーで勝負</option>|;
					}
					if ($rest_a > 0) {
						print qq|<option value="send_a">グーを渡す</option>|;
					}
					if ($rest_b > 0) {
						print qq|<option value="send_b">チョキを渡す</option>|;
					}
					if ($rest_c > 0) {
						print qq|<option value="send_c">パーを渡す</option>|;
					}
					if ($star > 1) {
						print qq|<option value="send_star">星を渡す</option>|;
					}
					print qq|</select>|;
					print qq|相手：|;
					&print_player_select('to');
					print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
					print qq|<input type="submit" value="送信" class="button_s"><br>|;
					print qq|</form>|;
				} else {
					if (($count > 1 && $star >= 4) ||$star >= 3) {
						print qq|<form method="$method" action="$this_script" name="form">|;
						print qq|<input type="hidden" name="mode" value="goal">|;
						print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
						print qq|<input type="submit" value="あがり" class="button_s"><br>|;
						print qq|</form>|;
					}
				}
			}
		}
	} else {
		print qq|乗船者募集中|;
		if ($participate) {
			print qq|あなたは乗船予\定です。|;
		} else {
			print qq|<form method="$method" action="$this_script" name="form">|;
			print qq|<input type="hidden" name="mode" value="participate">|;
			print qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass"><input type="hidden" name="guid" value="ON">|;
			print qq|<input type="submit" value="乗船" class="button_s"><br>|;
			print qq|</form>|;
		}
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

sub get_state {
	my @all_players = ();
	my $participate = 0;
	my $star;
	my $my_rest_a = 0;
	my $my_rest_b = 0;
	my $my_rest_c = 0;
	
	open my $fh, "< $all_member_file" or &error('参加者ﾌｧｲﾙが開けません'); 
	my $headline = <$fh>;
	my($play_year, $rest_a, $rest_b, $rest_c) = split /<>/, $headline;
	while (my $line = <$fh>) {
		chomp $line;
		if ($line) {
			push @all_players, $line;
			if ($line eq $m{name}) {
				$participate = 1;
			}
		}
	}
	close $fh;
	
	return ($play_year, $rest_a, $rest_b, $rest_c, $participate, @all_players);
}

sub get_my_state {
	my %stack = ();
	my @star = ();
	my @a = ();
	my @b = ();
	my @c = ();
	my @check = ();
	my @send = ();
	open my $fhm, "< $my_espoir_file" or &error('参加者ﾌｧｲﾙが開けません'); 
	my $headline = <$fhm>;
	my ($star, $rest_a, $rest_b, $rest_c, $count, $year, $check_h) = split /<>/, $headline;
	while (my $line = <$fh>) {
		my ($type, $name) = split /<>/, $line;
		if ($type eq '1') {
			push @star, $name;
		} elsif ($type eq '2') {
			push @a, $name;
		} elsif ($type eq '3') {
			push @b, $name;
		} elsif ($type eq '4') {
			push @c, $name;
		} elsif ($type eq '5') {
			push @check, $name;
		} else {
			push @send, $name;
		}
	}
	close $fhm;
	
	$stack{star} = \@star;
	$stack{a} = \@a;
	$stack{b} = \@b;
	$stack{c} = \@c;
	$stack{check} = \@check;
	$stack{send} = \@send;
	
	return ($rest_a, $rest_b, $rest_c, $star, $count, $year, $check_h, %stack);
}

sub participate {
	open my $fh, "< $all_member_file" or &error('参加者ﾌｧｲﾙが開けません'); 
	my $headline = <$fh>;
	my($play_year, $rest_a, $rest_b, $rest_c) = split /<>/, $headline;
	my @all_players = ();
	my $find = 0;
	while (my $line = <$fh>) {
		chomp $line;
		if ($line) {
			push @all_players, $line;
			if ($line eq $m{name}) {
				$find = 1;
			}
		}
	}
	close $fh;
	
	if (!$find && $m{coin} >= $rate) {
		&coin_move(-1 * $rate, $m{name}, 1);
		
		push @all_players, $m{name};
		
		if (@all_players >= $min_espoir) {
			if ($play_year != $w{year} + 1) {
				$play_year = $w{year} + 1;
				&system_comment("$play_yearにエスポワール<希望>は出港いたします。");
			}
			for my $en (@all_players) {
				my $en_id = unpack 'H*', $en;
				&change_my_status($en_id, 'year', $play_year);
			}
		}
		my $player_num = @all_players;
		my $cards = $player_num * 3;
		$headline = "$play_year<>$cards<>$cards<>$cards<>\n";
		
		unshift @all_players, $headline;
		
		open my $wfh, "> $all_member_file" or &error('参加者ﾌｧｲﾙが開けません'); 
		for my $line (@all_players) {
			print $wfh "$line\n";
		}
		close $wfh;
		&change_my_status($id, 'star', 3);
		&change_my_status($id, 'a', 3);
		&change_my_status($id, 'b', 3);
		&change_my_status($id, 'c', 3);
		&change_my_status($id, 'count_add', 1);
		&change_my_status($id, 'set', '');
		&clear_stack($id);
		return "$m{name}が乗船しました。";
	}
	return "";
}

sub send_star {
	my $to = shift;
	if ($to eq $m{name}) {
		return;
	}
	my $to_id = unpack 'H*', $to;
	&change_my_status($id, 'add_star', -1);
	&add_my_status_line($id, -1, $to);
	&add_my_status_line($to_id, 1, $m{name});
}

sub send_a {
	my $to = shift;
	if ($to eq $m{name}) {
		return;
	}
	my $to_id = unpack 'H*', $to;
	&change_my_status($id, 'add_a', -1);
	&add_my_status_line($id, -2, $to);
	&add_my_status_line($to_id, 2, $m{name});
}

sub send_b {
	my $to = shift;
	if ($to eq $m{name}) {
		return;
	}
	my $to_id = unpack 'H*', $to;
	&change_my_status($id, 'add_b', -1);
	&add_my_status_line($id, -3, $to);
	&add_my_status_line($to_id, 3, $m{name});
}

sub send_c {
	my $to = shift;
	if ($to eq $m{name}) {
		return;
	}
	my $to_id = unpack 'H*', $to;
	&change_my_status($id, 'add_c', -1);
	&add_my_status_line($id, -4, $to);
	&add_my_status_line($to_id, 4, $m{name});
}

sub receive {
	my $type = shift;
	my ($find, $name) = &remove_my_status_line($id, $type, '');
	if ($find) {
		my $from_id = unpack 'H*', $name;
		&remove_my_status_line($from_id, -1 * $type, $m{name});
		my $sta = $type == 1 ? 'star_add' :
					$type == 2 ? 'a_add' :
					$type == 3 ? 'b_add' :
					$type == 4 ? 'c_add' :
								'';
		&change_my_status($id, $sta, 1);
	}
}

sub refuse {
	my $type = shift;
	my ($find, $name) = &remove_my_status_line($id, $type, '');
	if ($find) {
		my $from_id = unpack 'H*', $name;
		&remove_my_status_line($from_id, -1 * $type, $m{name});
		my $sta = $type == 1 ? 'star_add' :
					$type == 2 ? 'a_add' :
					$type == 3 ? 'b_add' :
					$type == 4 ? 'c_add' :
								'';
		&change_my_status($from_id, $sta, 1);
	}
}

sub check_a {
	my $to = shift;
	if ($to eq $m{name}) {
		return;
	}
	my $to_id = unpack 'H*', $to;
	my ($rest_a, $rest_b, $rest_c, $star, $count, $year, $check_h, %stack) = &get_my_state;
	if ($rest_a > 0 && !$check_h) {
		&change_my_status($id, 'set', 1);
		&add_my_status_line($id, -5, $to);
		&add_my_status_line($to_id, 5, $m{name});
		&change_my_status($id, 'add_a', -1);
	}
	return 'チェック';
}

sub check_b {
	my $to = shift;
	if ($to eq $m{name}) {
		return;
	}
	my $to_id = unpack 'H*', $to;
	my ($rest_a, $rest_b, $rest_c, $star, $count, $year, $check_h, %stack) = &get_my_state;
	if ($rest_b > 0 && !$check_h) {
		&change_my_status($id, 'set', 2);
		&add_my_status_line($id, -5, $to);
		&add_my_status_line($to_id, 5, $m{name});
		&change_my_status($id, 'add_b', -1);
	}
	return 'チェック';
}

sub check_c {
	my $to = shift;
	if ($to eq $m{name}) {
		return;
	}
	my $to_id = unpack 'H*', $to;
	my ($rest_a, $rest_b, $rest_c, $star, $count, $year, $check_h, %stack) = &get_my_state;
	if ($rest_c > 0 && !$check_h) {
		&change_my_status($id, 'set', 3);
		&add_my_status_line($id, -5, $to);
		&add_my_status_line($to_id, 5, $m{name});
		&change_my_status($id, 'add_c', -1);
	}
	return 'チェック';
}

sub recheck {
	my $hand = shift;
	my ($rest_a, $rest_b, $rest_c, $star, $count, $year, $check_h, %stack) = &get_my_state;
	if (($hand == 1 && $rest_a <= 0) || ($hand == 2 && $rest_b <= 0) || ($hand == 3 && $rest_c <= 0)) {
		return;
	}
	
	my $type = 5;
	my ($find, $name) = &remove_my_status_line($id, $type, '');
	if ($find) {
		my $from_id = unpack 'H*', $name;
		&remove_my_status_line($from_id, -1 * $type, $m{name});
		my $y_hand = &change_my_status($from_id, 'set', '');
		&system_comment('セット');
		my $win = 0;
		my $omes = "オープン<br>$m{name}:";
		if ($hand == 1) {
			&change_my_status($id, 'add_a', -1);
			$omes .= 'グー vs ';
			if ($y_hand == 1) {
				$omes .= "$name:グー<br>あいこ";
			} elsif ($y_hand == 2) {
				$omes .= "$name:チョキ<br>$m{name}勝利";
				$win = 1;
			} else {
				$omes .= "$name:パー<br>$name勝利";
				$win = -1;
			}
		} elsif ($hand == 2) {
			&change_my_status($id, 'add_b', -1);
			$omes .= 'チョキ vs ';
			if ($y_hand == 1) {
				$omes .= "$name:グー<br>$name勝利";
				$win = -1;
			} elsif ($y_hand == 2) {
				$omes .= "$name:チョキ<br>あいこ";
			} else {
				$omes .= "$name:パー<br>$m{name}勝利";
				$win = 1;
			}
		} else {
			&change_my_status($id, 'add_c', -1);
			$omes .= 'パー vs ';
			if ($y_hand == 1) {
				$omes .= "$name:グー<br>$m{name}勝利";
				$win = 1;
			} elsif ($y_hand == 2) {
				$omes .= "$name:チョキ<br>$name勝利";
				$win = -1;
			} else {
				$omes .= "$name:パー<br>あいこ";
			}
		}
		&decrease_all($hand);
		&decrease_all($y_hand);
		&system_comment($omes);
		if ($win != 0) {
			&change_my_status($id, 'add_star', $win);
			&change_my_status($from_id, 'add_star', -1 * $win);
		}
	}
}

sub uncheck {
	my ($find, $name) = &remove_my_status_line($id, 5, '');
	if ($find) {
		my $from_id = unpack 'H*', $name;
		&remove_my_status_line($from_id, -5, $m{name});
		my $y_hand = &change_my_status($from_id, 'set', '');
		my $sta = $y_hand == 1 ? 'a_add' :
					$y_hand == 2 ? 'b_add' :
					$y_hand == 3 ? 'c_add' :
								'';
		&change_my_status($from_id, $sta, 1);
	}
	return 'ン拒否するゥ';
}

sub goal {
	my ($rest_a, $rest_b, $rest_c, $star, $count, $year, $check_h, %stack) = &get_my_state;
	my $need_star = 3;
	if ($count> 1) {
		$need_star = 4;
	}
	
	if (@{$stack{star}}) {
		return '星を受け取るか拒否してください。';
	}
	if (@{$stack{a}}) {
		return 'グーを受け取るか拒否してください。';
	}
	if (@{$stack{b}}) {
		return 'チョキを受け取るか拒否してください。';
	}
	if (@{$stack{c}}) {
		return 'パーを受け取るか拒否してください。';
	}
	if (@{$stack{check}}) {
		return '勝負を受け取るか拒否してください。';
	}
	if (@{$stack{send}}) {
		return '送った相手が受け取っていないか拒否していません。';
	}
	
	if ($rest_a <= 0 && $rest_b <= 0 && $rest_c <= 0 && $star >= $need_star && !$check_h) {
		my $else_star = $star - $need_star;
		my $recv = $rate * (3 + $else_star);
		while ($recv > $overflow) {
			$recv -= $bonus_coin;
			&bonus($m{name}, '', '');
		}
		return '';
	}
	return '終了条件を満たしていません。';
}

sub lose {
	my $name = shift;
	
}

sub add_my_status_line {
	my $to_id = shift;
	my $type = shift;
	my $name = shift;
	
	unless (-f "$userdir/$change_id/espoir.cgi") {
		open my $fh, "> $userdir/$change_id/espoir.cgi" or &error('賭けﾌｧｲﾙの書き込みに失敗しました');
		print $fh "<>0<>0<>0<>0<><><>\n";
		close $fh;
	}
	
	my @lines = ();
	open my $fhm, "< $userdir/$to_id/espoir.cgi" or &error('参加者ﾌｧｲﾙが開けません'); 
	my $headline = <$fhm>;
	push @lines, $head_line;
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	close $fhm;
	
	push @lines, "$type<>$name<>\n";
	
	open my $fhw, "> $userdir/$to_id/espoir.cgi" or &error('参加者ﾌｧｲﾙが開けません'); 
	print $fhw @lines;
	close $fhm;
}

sub remove_my_status_line {
	my $to_id = shift;
	my $rm_name = shift;
	my $type = shift;
	
	unless (-f "$userdir/$change_id/espoir.cgi") {
		open my $fh, "> $userdir/$change_id/espoir.cgi" or &error('賭けﾌｧｲﾙの書き込みに失敗しました');
		print $fh "<>0<>0<>0<>0<><><>\n";
		close $fh;
	}
	
	my @lines = ();
	open my $fhm, "< $userdir/$to_id/espoir.cgi" or &error('参加者ﾌｧｲﾙが開けません'); 
	my $headline = <$fhm>;
	push @lines, $head_line;
	
	my $find = 0;
	while (my $line = <$fh>) {
		my ($t, $n) = split /<>/, $line;
		if (!$find && $t eq $type && (!$rm_name || $n eq $rm_name)) {
			$find = 1;
			$rm_name = $n;
		} else {
			push @lines, $line;
		}
	}
	close $fhm;
	
	open my $fhw, "> $userdir/$to_id/espoir.cgi" or &error('参加者ﾌｧｲﾙが開けません'); 
	print $fhw @lines;
	close $fhm;
	
	return ($find, $rm_name);
}

sub change_my_status {
	my $change_id = shift;
	my $key = shift;
	my $value = shift;
	my $ret = '';
	
	unless (-f "$userdir/$change_id/espoir.cgi") {
		open my $fh, "> $userdir/$change_id/espoir.cgi" or &error('賭けﾌｧｲﾙの書き込みに失敗しました');
		print $fh "<>0<>0<>0<>0<><><>\n";
		close $fh;
	}
	
	my @lines = ();
	open my $fhm, "< $userdir/$change_id/espoir.cgi" or &error('参加者ﾌｧｲﾙが開けません'); 
	my $headline = <$fhm>;
	my($star, $rest_a, $rest_b, $rest_c, $count, $year, $check_h) = split /<>/, $headline;
	if ($key eq 'star') {
		$star = $value;
	} elsif ($key eq 'star_add') {
		$star += $value;
	} elsif ($key eq 'a') {
		$rest_a = $value;
	} elsif ($key eq 'a_add') {
		$rest_a += $value;
	} elsif ($key eq 'b') {
		$rest_b = $value;
	} elsif ($key eq 'b_add') {
		$rest_b += $value;
	} elsif ($key eq 'c') {
		$rest_c = $value;
	} elsif ($key eq 'c_add') {
		$rest_c += $value;
	} elsif ($key eq 'count_add') {
		$count += $value;
	} elsif ($key eq 'year') {
		$year = $value;
	} elsif ($key eq 'set') {
		$ret = $check_h;
		$check_h = $value;
	}
	push @lines, "$star<>$rest_a<>$rest_b<>$rest_c<>$count<>$year<>$check_h<>\n";
	while (my $line = <$fh>) {
		push @lines, $line;
	}
	close $fhm;
	
	open my $fhw, "> $userdir/$change_id/espoir.cgi" or &error('参加者ﾌｧｲﾙが開けません'); 
	print $fhw @lines;
	close $fhm;
	
	return $ret;
}
sub clear_stack {
	my $clear_id = shift;
	
	unless (-f "$userdir/$clear_id/espoir.cgi") {
		open my $fh, "> $userdir/$clear_id/espoir.cgi" or &error('賭けﾌｧｲﾙの書き込みに失敗しました');
		print $fh "<>0<>0<>0<>0<><><>\n";
		close $fh;
	}
	
	my @lines = ();
	open my $fhm, "< $userdir/$clear_id/espoir.cgi" or &error('参加者ﾌｧｲﾙが開けません'); 
	my $headline = <$fhm>;
	push @lines, $headline;
	close $fhm;
	
	open my $fhw, "> $userdir/$clear_id/espoir.cgi" or &error('参加者ﾌｧｲﾙが開けません'); 
	print $fhw @lines;
	close $fhm;
}

sub decrease_all {
	my $hand = shift;
	
	my @all_players = ();
	
	open my $fh, "< $all_member_file" or &error('参加者ﾌｧｲﾙが開けません'); 
	my $headline = <$fh>;
	my($play_year, $rest_a, $rest_b, $rest_c) = split /<>/, $headline;
	while (my $line = <$fh>) {
		push @all_players, $line;
	}
	close $fh;
	if ($hand == 1) {
		$rest_a--;
	} elsif ($hand == 2) {
		$rest_b--;
	} elsif ($hand == 3) {
		$rest_c--;
	}
	unshift @all_players, "$play_year<>$rest_a<>$rest_b<>$rest_c<>\n";

	open my $fhw, "> $all_member_file" or &error('参加者ﾌｧｲﾙが開けません'); 
	print $fhw @all_players;
	close $fhw;
}

sub print_player_select {
	my $name = shift;

	my @all_players = ();
	open my $fh, "< $all_member_file" or &error('参加者ﾌｧｲﾙが開けません'); 
	my $headline = <$fh>;
	my($play_year, $rest_a, $rest_b, $rest_c) = split /<>/, $headline;
	while (my $line = <$fh>) {
		push @all_players, $line;
	}
	close $fh;

	print qq|<select name="$name">|;
	for my $pl (@all_players) {
		chomp $pl;
		if ($pl) {
			print qq|<option value="$pl">$pl</option>|;
		}
	}
	print qq|</select>|;
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
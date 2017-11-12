my $this_file = "$logdir/auction.cgi";
#=================================================
# ｵｰｸｼｮﾝ Created by Merino
#=================================================
require "$datadir/buyable.cgi";

# 拘束中の行動用関数
sub is_rest { return $m{lib_r} eq 'shopping_auction'; } # 拘束中の行動か
sub set_tp { (&is_rest ? $m{tp_r} : $m{tp}) = shift; } # 拘束中・非拘束中のtpｾｯﾀｰ
sub get_tp { return &is_rest ? $m{tp_r} : $m{tp}; } # 拘束中・非拘束中のｹﾞｯﾀｰ
sub refresh_r { $m{lib_r} = $m{tp_r} = ''; } # refreshの拘束中版

# 拘束中と同じ行動を非拘束中にした場合、拘束中の方をｷｬﾝｾﾙ
&refresh_r if $m{lib_r} eq $m{lib};

# 落札時間(日)
my $auction_limit_day = 3;

# 最大出品数
my $max_auction = 30;

# 出品禁止ｱｲﾃﾑ
my %taboo_items = (
	# ﾌﾞﾛﾝｽﾞｿｰﾄﾞ, ﾛﾝｸﾞｽﾋﾟｱ, ﾊﾞﾄﾙｱｸｽ, ﾌｧｲｱｰ, ｳｨﾝﾄﾞ, ｻﾝﾀﾞｰ,ｽﾘﾝｸﾞｼｮｯﾄ
	# ｼﾞｬﾝｸｼｮｯﾌﾟで手に入る物で出品枠を埋める荒らしへの対策だと思われる
	wea => [1,6,11,16,21,26,34], # 武器
	egg => [], # ﾀﾏｺﾞ
	pet => [], # ﾍﾟｯﾄ
	gua => [], # 防具
);


#=================================================
# 利用条件
#=================================================
sub is_satisfy {
	if ($m{shogo} eq $shogos[1][0] || $m{shogo_t} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]の方はお断りしています<br>";

		if (&is_rest) {
			&refresh_r;
		}
		else {
			&refresh;
			$m{lib} = 'shopping';
		}

		&n_menu;
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if (&get_tp > 1) {
		$mes .= '他に何かしますか?<br>';
		&set_tp(1);
	}
	else {
		$mes .= 'ｵｰｸｼｮﾝ会場に来ました<br>何をしますか?<br>';
	}
	if (&is_rest) {
		&menu('やめる','入札する');
	}
	else {
		&menu('やめる','入札する','出品する');
	}
}
sub tp_1 {
	return if &is_ng_cmd(1,2);
	
	&set_tp($cmd * 100);
	&{ 'tp_'.&get_tp };
}

#=================================================
# 入札
#=================================================
sub tp_100 {
	$layout = 1;
	
	$mes .= qq|ｵｰｸｼｮﾝの落札日数は、出品日から $auction_limit_day日前後です<br>|;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" id="no_0" name="cmd" value="0" checked><label for="no_0">やめる</label><br>|;
 	$mes .= $is_mobile ? qq|<hr>落札品/入札額/即決額/入札者/出品者<br>|
 		: qq|<table class="table1" cellpadding="3"><tr><th>落札品</th><th>入札額</th><th>即決額</th><th>入札者</th><th>出品者</th><th>状態</th><th>入札可能\額<br></th>|;

	open my $fh, "< $this_file" or &error("$this_fileが読み込めません");
	$m{total_auction} = 0;
	while (my $line = <$fh>) {
		my($bit_time, $no, $kind, $item_no, $item_c, $item_lv, $from_name, $to_name, $item_price, $buyout_price) = split /<>/, $line;
		my $item_title = &get_item_name($kind, $item_no, $item_c, $item_lv);
		my $item_state = $time + 3600 * 24 > $bit_time ? "そろそろ":
						$time + ($auction_limit_day - 1) * 3600 * 24 > $bit_time ? "まだまだ":"new";
		unless($buyout_price){
			$buyout_price = 'なし';
		}
		my $next_min_price = int($item_price * 1.2);
		$mes .= $is_mobile ? qq|<hr><input type="radio" name="cmd" value="$no">$item_title/$item_price G/即$buyout_price G/$to_name/$from_name/$item_state<br>|
			: qq|<tr><td><input type="radio" id="$no" name="cmd" value="$no"><label for="$no">$item_title</label></td><td align="right">$item_price G</td><td align="right">$buyout_price G</td><td>$to_name</td><td>$from_name</td><td>$item_state<br></td><td>$next_min_price</td></tr>|;
		$m{total_auction} += $item_price if ($to_name eq $m{name} && $from_name ne $m{name});
	}
	close $fh;
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<p>入札金額：<input type="text" name="money" value="0" class="text_box1" style="text-align:right" class="text1">G</p>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="入札する" class="button1"></p></form>|;
	
	&set_tp(&get_tp + 10);
}
sub tp_110 {
	$in{money} = int($in{money});
	if ($m{money} < $in{money} + $m{total_auction}) {
		$mes .= 'そんなにお金を持っていません<br>';
	}
	elsif ($cmd && $in{money} && $in{money} !~ /[^0-9]/) {
		my $is_rewrite = 0;
		my $is_sokketsu = 0;
		my @news_messages = ();
		my @lines = ();
		open my $fh, "+< $this_file" or &error("$this_fileが開けません");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($bit_time, $no, $kind, $item_no, $item_c, $item_lv, $from_name, $to_name, $item_price, $buyout_price) = split /<>/, $line;
			next unless $item_no; # どういう経緯で起きたのか分からんがデータなしが落札されたので弾く
			if ($no eq $cmd) {
				my $need_money = int($item_price * 1.2);
				if ($buyout_price && $need_money > $buyout_price) {
					$need_money = $buyout_price;
				}
				if ( $in{money} >= $need_money && &is_buyable($kind, $item_no) ) {
					my $item_title = &get_item_name($kind, $item_no, $item_c, $item_lv);

					$m{total_auction} += $in{money};
					$mes .= "$item_titleに $in{money} Gで入札しました<br>";
					if($buyout_price && $in{money} >= $buyout_price){
						my $to_id = unpack 'H*', $m{name};
						if(-e "$userdir/$to_id/user.cgi"){
							&send_item($m{name}, $kind, $item_no, $item_c, $item_lv, 1);
						}
						&send_money($m{name}, 'ｵｰｸｼｮﾝ会場', "-$in{money}");
						&send_money($from_name, 'ｵｰｸｼｮﾝ会場', $in{money});
						&sale_data_log($kind, $item_no, $item_c, $item_lv, $in{money}, 3);
						$mes .= "即決価格を提示しました<br>";
						push @news_messages, "$from_nameの出品した$item_titleを$m{name}が $in{money} G(即決)で落札しました";
#						&write_send_news("$from_nameの出品した$item_titleを$m{name}が $in{money} G(即決)で落札しました");
						&send_twitter("$from_nameの出品した$item_titleを$m{name}が $in{money} G(即決)で落札しました");
						$is_sokketsu = 1;
						$is_rewrite = 1;
					}else{
						$line = "$bit_time<>$no<>$kind<>$item_no<>$item_c<>$item_lv<>$from_name<>$m{name}<>$in{money}<>$buyout_price<>\n";
						$is_rewrite = 1;
					}
				}
				else {
					$mes .= "入札は現在の落札額の1.2倍以上の金額( $need_money G)が必要です<br>";
				}
				unless($is_sokketsu){
					push @lines, $line;
				}
			}
			# 落札処理
			elsif ($time > $bit_time) {
				my $item_title = &get_item_name($kind, $item_no, $item_c, $item_lv);
				
				my $to_id = unpack 'H*', $to_name;
				if(-e "$userdir/$to_id/user.cgi"){
					&send_item($to_name, $kind, $item_no, $item_c, $item_lv, 1);
				}
				&send_money($to_name, 'ｵｰｸｼｮﾝ会場', "-$item_price");
				&send_money($from_name, 'ｵｰｸｼｮﾝ会場', $item_price);
				&sale_data_log($kind, $item_no, $item_c, $item_lv, $item_price, 2);
				push @news_messages, "$from_nameの出品した$item_titleを$to_nameが $item_price Gで落札しました";
#				&write_send_news("$from_nameの出品した$item_titleを$to_nameが $item_price Gで落札しました");
				&send_twitter("$from_nameの出品した$item_titleを$to_nameが $item_price Gで落札しました");
				$is_rewrite = 1;
			}
			else {
				push @lines, $line;
			}
		} # while (my $line = <$fh>) {
		if ($is_rewrite) {
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
		}
		close $fh;

		for my $news_message (@news_messages) {
			&write_send_news($news_message);
		}
	}
	else {
		$mes .= 'やめました<br>';
	}
	
	&begin;
}

#=================================================
# 出品
#=================================================
sub tp_200 {
	if (&is_rest) {
		$mes .= '拘束中に出品することはできません';
		&refresh_r;
		return;
	}
	$layout = 1;
	$mes .= 'どれを出品しますか?<br>';

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" id="no_0" name="cmd" value="0" checked><label for="no_0">やめる</label><br>|;
	$mes .= qq|<input type="radio" id="no_1" name="cmd" value="1"><label for="no_1">$weas[$m{wea}][1]★$m{wea_lv}($m{wea_c})</label><br>| if $m{wea};
	$mes .= qq|<input type="radio" id="no_2" name="cmd" value="2"><label for="no_2">$eggs[$m{egg}][1]($m{egg_c})</label><br>| if $m{egg};
	$mes .= qq|<input type="radio" id="no_3" name="cmd" value="3"><label for="no_3">$pets[$m{pet}][1]★$m{pet_c}</label><br>| if $m{pet} > 0;
	$mes .= qq|<input type="radio" id="no_4" name="cmd" value="4"><label for="no_4">$guas[$m{gua}][1]</label><br>| if $m{gua};
	$mes .= qq|入札期限<br>|;
	$mes .= qq|<input type="radio" id="no_5" name="tlimit" value="0" checked><label for="no_5">普通</label><br>|;
	$mes .= qq|<input type="radio" id="no_6" name="tlimit" value="1"><label for="no_6">長め</label><br>|;
	$mes .= qq|<input type="radio" id="no_7" name="tlimit" value="2"><label for="no_7">短め</label><br>|;
	$mes .= qq|<p>初期金額<input type="text" name="price" value="0" class="text_box1" style="text-align:right">G</p>|;
	$mes .= qq|<p>即決金額<input type="text" name="buyout_price" value="0" class="text_box1" style="text-align:right">G</p>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="出品する" class="button1"></p></form>|;
	
	&set_tp(&get_tp + 10);
}
sub tp_210 {
	return if &is_ng_cmd(1..4);
	
	my $is_find = 0;
	my @lines = ();
	open my $fh, "< $this_file" or &error("$this_file が開けませんでした");
	while (my $line = <$fh>) {
		my($name) = (split /<>/, $line)[6];
		if (!$is_find && $m{name} eq $name) {
			$is_find = 1;
		}
		push @lines, $line;
	}
	close $fh;
	
	if ($is_find) {
		$mes .= '出品しているものが落札されるまで、出品することはできません<br>';
	}
	elsif (@lines >= $max_auction) {
		$mes .= '現在、出品の受付はしておりません<br>出品数が減ってから再度申\し込みください<br>';
	}
	elsif ($in{price} =~ /[^0-9]/ || $in{price} >= 4999999 || $in{price} < 5) {
		$mes .= '値段は 5 G以上 499万9999 G以内にする必要があります<br>';
	}
	elsif ($in{buyout_price} =~ /[^0-9]/ || $in{buyout_price} >= 4999999) {
		$mes .= '即決値段は 499万9999 G以内にする必要があります<br>';
	}
	elsif ( ($cmd eq '1' && $m{wea})
		 || ($cmd eq '2' && $m{egg})
		 || ($cmd eq '3' && $m{pet})
		 || ($cmd eq '4' && $m{gua}) ) {
			
			my @kinds = ('', 'wea', 'egg', 'pet', 'gua');
			for my $taboo_item (@{ $taboo_items{ $kinds[$cmd] } }) {
				if ($taboo_item eq $m{ $kinds[$cmd] }) {
					my $t_item_name = $cmd eq '1' ? $weas[$m{wea}][1]
									: $cmd eq '2' ? $eggs[$m{egg}][1]
									: $cmd eq '3' ? $pets[$m{pet}][1]
									:               $guas[$m{gua}][1]
									;
					$mes .= "$t_item_nameは出品禁止ｱｲﾃﾑとなっております<br>";
					&begin;
					return;
				}
			}
			
			my $item_price = $in{price} || 0;
			my $buyout_price = $in{buyout_price} || 0;
			my $item_no = $m{ $kinds[$cmd]       };
			my $item_c  = $m{ $kinds[$cmd].'_c'  } || 0;
			my $item_lv = $m{ $kinds[$cmd].'_lv' } || 0;
			
			if ($cmd eq '1' && $m{wea}) {
				if($m{wea_name}){
					$m{wea} = 32;
					$m{wea_c} = 0;
					$m{wea_lv} = 0;
					$mes .= "持ち主の手を離れた途端$m{wea_name}はただの$weas[$m{wea}][1]になってしまった<br>";
					$m{wea_name} = "";
				}
				&mes_and_send_news("$weas[$m{wea}][1]を出品しました");
				&send_twitter("$weas[$m{wea}][1]を出品しました", 1);
				$m{wea} = $m{wea_c} = $m{wea_lv} = 0;
			}
			elsif ($cmd eq '2' && $m{egg}) {
				&mes_and_send_news("$eggs[$m{egg}][1]を出品しました");
				&send_twitter("$eggs[$m{egg}][1]を出品しました", 1);
				$m{egg} = $m{egg_c} = 0;
			}
			elsif ($cmd eq '3' && $m{pet}) {
				&mes_and_send_news("$pets[$m{pet}][1]★$m{pet_c}を出品しました");
				&send_twitter("$pets[$m{pet}][1]★$m{pet_c}を出品しました", 1);
				&remove_pet;
			}
			elsif ($cmd eq '4' && $m{gua}) {
				&mes_and_send_news("$guas[$m{gua}][1]を出品しました");
				&send_twitter("$guas[$m{gua}][1]を出品しました", 1);
				$m{gua} = 0;
			}
			
			my $bit_time = $time + int( $auction_limit_day * 3600 * 24 + rand(3600) ); # 入札時間を１時間程度ばらけさす
			$bit_time += int( 3600 * 24 + rand(3600) ) if $in{tlimit} eq '1'; 
			$bit_time -= int( 3600 * 24 + rand(3600) ) if $in{tlimit} eq '2'; 
			my($last_no) = (split /<>/, $lines[-1])[1];
			++$last_no;
			open my $fh2, ">> $this_file" or &error("$this_file が開けませんでした");
			print $fh2 "$bit_time<>$last_no<>$cmd<>$item_no<>$item_c<>$item_lv<>$m{name}<>$m{name}<>$item_price<>$buyout_price<>\n";
			close $fh2;
	}
	else {
		$mes .= 'やめました<br>';
	}
	
	&begin;
}

sub is_buyable{
	my ($kind, $item_no) = @_;
	return 1;
	if($m{is_full}){
		if($kind eq '1'){
			for my $i (@full_buyable_wea){
				if($item_no == $i){
					return 1;
				}
			}
			return 0;
		}elsif($kind eq '2'){
			for my $i (@full_buyable_egg){
				if($item_no == $i){
					return 1;
				}
			}
			return 0;
		}else{
			for my $i (@full_buyable_pet){
				if($item_no == $i){
					return 1;
				}
			}
			return 0;
		}
	}
	return 1;
}

1; # 削除不可

use Time::HiRes;
my $this_file = "$userdir/$id/depot.cgi";
my $this_log = "$userdir/$id/depot_log.cgi";
my $this_lock_file = "$userdir/$id/depot_lock.cgi";
#=================================================
# �a���菊 Created by Merino
#=================================================

# �ő�ۑ���
my $max_depot = $m{sedai} > 7 ? 50 : $m{sedai} * 5 + 15;
$max_depot += $m{depot_bonus} if $m{depot_bonus};

# �e�����̊J�n���ɑq�ɂ̎C��؂���s���Ə����̌��Ԃőq���ް��������������Ă����ꍇ�ɈӐ}���ʱ��т̏������N���邽�߁A�C��؂菈�����J�n���ł͂Ȃ����O�ɕύX
# ��F�����o����ʂ��J������ɉו����͂����ꍇ�Aհ�ް�ͱ��т�������������ł������Ă����߯Ă��������͂����ו��������ɒǉ������
# �C��؂菈��������͈̂����o�������Ɛ������������@��ɔ��邩�̂Ă邩���đq�ɂ��J����ΎC��؂�Ώۂ̱��т���ׂł���
# �C��؂�Ώۂ̱��т̓��b�N�𖳎����Ĕ�������̂Ă���ł���
my $lost_depot = $max_depot * 2;

# ����ɑ���Ƃ��̎萔��(����)
my $need_money = 100;

# ����ɑ���Ƃ��̎萔��(����)
my $need_money_other = 1000;

# ����l�i
my $sall_price = 100;

# ���t�𒴂�����������è��(���o���A���鎞�Ɍ��炳���)
my $penalty_money = $m{sedai} > 10 ? 3000 : $m{sedai} * 300;

# ����ɑ��鎞�ɕK�v������(������1���㎞�̂�)
my $need_lv = 10;

# ����ɑ���̋֎~�ȱ���
my %taboo_items = (
	wea => [32,], # ����
	egg => [], # �Ϻ�
	pet => [127,188], # �߯�
	gua => [], # �h��
);

my @magic_words = ('a'..'z', 'A'..'Z', 0..9);

#================================================
sub begin {

	local $magic_word = '';
	$magic_word .= $magic_words[int(rand($#magic_words+1))] for (0 .. 12);
	$m{magic_word} = $magic_word;

	if (-f "$userdir/$id/depot_flag.cgi") {
		unlink "$userdir/$id/depot_flag.cgi";
	}
	unless (-f $this_lock_file) {
		open my $lfh, "> $this_lock_file" or &error("$this_lock_file���J���܂���");
		close $lfh;
	}
	if ($m{tp} > 1) {
		$mes .= "���ɉ������܂���?<br>";
		$m{tp} = 1;
	}
	else {
		$mes .= "�����͗a���菊�ł��B$max_depot�܂ŗa���邱�Ƃ��ł��܂�<br>";
		$mes .= "$max_depot�𒴂��Ă���ꍇ�́A$penalty_money G�̔������x�����Ă��炢�܂�<br>";
		$mes .= "�ǂ����܂���?<br>";
	}
	&menu('��߂�', '���o��', '�a����', '��������', '����ɑ���', '�ꊇ���p', '�̂Ă�', '���b�N��������', '����');
}
sub tp_1 {
	unless ($in{magic_word} eq $m{magic_word}) {
		$mes .= "�s���ȏ����ɂ��q�ɂ̑���𒆒f���܂���<br>";
		&begin;
		return;
	}
	return if &is_ng_cmd(1..8);

	$m{tp} = $cmd * 100;
	&{ 'tp_'. $m{tp} };
}

#=================================================
# ���o��
#=================================================
sub tp_100 {
	unless ($in{magic_word} eq $m{magic_word}) {
		$mes .= "�s���ȏ����ɂ��q�ɂ̑���𒆒f���܂���<br>";
		&begin;
		return;
	}

	my $no = $_[0];
	$layout = 2;
	my($count, $sub_mes) = &radio_my_depot($no);

	my $lost_mes = '';
	my $lost_count = ($count - $lost_depot) < 0 ? 0 : $count - $lost_depot;
	$lost_mes = qq| / <font color="#FF0000">$lost_count</font>| if $lost_count;
	$count -= $lost_count;
	$mes .= "�ǂ�����o���܂���? [ $count / $max_depot$lost_mes ]<br>";
	$mes .= $sub_mes;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="hidden" name="magic_word" value="$in{magic_word}">|; # ���������Ȃ����߂̈ꎞ�L�[
	$mes .= $is_mobile ? qq|<p><input type="submit" value="���o��" class="button1" accesskey="#"></p>|:
		qq|<p><input type="submit" value="���o��" class="button1"></p>|;
	$mes .= qq|<label><input type="checkbox" id="pet_summary" name="show_summary" value="1">�߯Ă̌��ʂ��m�F����</label></form>|;
	$m{tp} += 10;
}
sub tp_110 {
	unless ($in{magic_word} eq $m{magic_word}) {
		$mes .= "�s���ȏ����ɂ��q�ɂ̑���𒆒f���܂���<br>";
		&begin;
		return;
	}
	else { # �����ŃL�[���ς�����u�Ԃ��炠�Ƃɑ����Ăяo�����e����邪�A�L�[���ς��u�Ԃɓ�����Ƃ����炭���Ǔ����������ꂻ���ȋC������
		my $magic_word = '';
		$magic_word .= $magic_words[int(rand($#magic_words+1))] for (0 .. 12);
		$in{magic_word} = $magic_word;
		$m{magic_word} = $magic_word;
		&write_user;
	}
	if ($in{show_summary} && $cmd && $cmd <= $lost_depot) { # �߯Ă̐���Ӱ�ނ���\���ް��ɃA�N�Z�X���ĂȂ�
		require './data/pet.cgi';
		my $count = 0;
		my $new_line = '';
		open my $fh, "< $this_file" or &error("$this_file���J���܂���");
		while (my $line = <$fh>) {
			my($rkind, $ritem_no, $ritem_c, $ritem_lv) = split /<>/, $line;
			++$count;
			if (!$new_line && $cmd eq $count) {
				$new_line = $line;
				my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
				my $item_name = &get_item_name($kind, $item_no);
				if($kind eq '3' && $item_no > 0) {
					$mes .= "$item_name�F$pet_effects[$item_no]<br>";
					last;
				}
				else {
					$mes .= "$item_name���߯Ăł͂���܂���<br>";
					last;
				}
			}
		}
		close $fh;

		$m{tp} -= 10;
		&{ 'tp_'. $m{tp} }($cmd);
		return;
	}
	else { # �����o��Ӱ��
		if ($cmd && $cmd <= $lost_depot) { # ��\���ް��ɃA�N�Z�X���ĂȂ�
			my $count = 0;
			my $new_line = '';
			my $add_line = '';
			my $depot_line = '';
			my @lines = ();
			my $l_mes = "";
			open my $fh, "+< $this_file" or &error("$this_file���J���܂���");
			eval { flock $fh, 2; };
			while (my $line = <$fh>) {
				if ($in{magic_word} ne $m{magic_word}) { # �����Œe���ƌ��ʃe�L�����炵�� �s��炵����̌�����
					$mes = "�s���ȏ����ɂ��q�ɂ̑���𒆒f���܂���<br>";
					close $fh;
					&begin;
					return;
				}
				my($rkind, $ritem_no, $ritem_c, $ritem_lv) = split /<>/, $line;
				$depot_line .= "$rkind,$ritem_no,$ritem_c,$ritem_lv<>";
				++$count;
				if (!$new_line && $cmd eq $count) {
					$new_line = $line;
					my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
					$depot_line .= "$kind,$item_no,$item_c,$item_lv<>";
					if ($kind eq '1' && $m{wea}) {
						if($m{wea_name}){
							$m{wea} = 32;
							$m{wea_c} = 0;
							$m{wea_lv} = 0;
							$mes .= "������̎�𗣂ꂽ�r�[$m{wea_name}�͂�����$weas[$m{wea}][1]�ɂȂ��Ă��܂���<br>";
							$m{wea_name} = "";
						}
						$add_line = "$kind<>$m{wea}<>$m{wea_c}<>$m{wea_lv}<>\n";
						$mes .= $l_mes = "$weas[$m{wea}][1]��a��";
					}
					elsif ($kind eq '2' && $m{egg}) {
						$add_line = "$kind<>$m{egg}<>$m{egg_c}<>0<>\n";
						$mes .= $l_mes = "$eggs[$m{egg}][1]��a��";
					}
					elsif($kind eq '3' && $m{pet} > 0) {
						$add_line = "$kind<>$m{pet}<>$m{pet_c}<>0<>\n";
						$mes .= $l_mes = "$pets[$m{pet}][1]��$m{pet_c}��a��";
					}
					elsif($kind eq '4' && $m{gua}) {
						$add_line = "$kind<>$m{gua}<>0<>0<>\n";
						$mes .= $l_mes = "$guas[$m{gua}][1]��a��";
					}
				}
				elsif ($count <= $lost_depot) { # �C��؂菈��
					push @lines, $line;
				}
			}
			if ($in{magic_word} ne $m{magic_word}) { # �������Ԃ�v��Ȃ��H �O�̂���
				$mes = "�s���ȏ����ɂ��q�ɂ̑���𒆒f���܂���<br>";
				close $fh;
				&begin;
				return;
			}
			elsif ($new_line) {
				push @lines, $add_line if $add_line;
				seek  $fh, 0, 0;
				truncate $fh, 0; 
				print $fh @lines;
				close $fh;

				my $s_mes;
				my($kind, $item_no, $item_c, $item_lv) = split /<>/, $new_line;
				if ($kind eq '1') {
					$m{wea}    = $item_no;
					$m{wea_c}  = $item_c;
					$m{wea_lv} = $item_lv;
					$mes .= "$weas[$m{wea}][1]�����o���܂���<br>";
					$l_mes .= $s_mes = "$weas[$m{wea}][1]";
				}
				elsif ($kind eq '2') {
					$m{egg}    = $item_no;
					$m{egg_c}  = $item_c;
					$mes .= "$eggs[$m{egg}][1]�����o���܂���<br>";
					$l_mes .= $s_mes = "$eggs[$m{egg}][1]";
				}
				elsif ($kind eq '3') {
					$m{pet}    = $item_no;
					$m{pet_c}  = $item_c;
					$mes .= "$pets[$m{pet}][1]��$m{pet_c}�����o���܂���<br>";
					$l_mes .= $s_mes = "$pets[$m{pet}][1]��$m{pet_c}";

					&get_icon_pet;
				}
				elsif ($kind eq '4') {
					$m{gua}    = $item_no;
					$mes .= "$guas[$m{gua}][1]�����o���܂���<br>";
					$l_mes .= $s_mes = "$guas[$m{gua}][1]";
				}
				my($tmin,$thour,$tmday,$tmon,$tyear) = (localtime($time))[1..4];
				$tdate = sprintf("%d/%d %02d:%02d", $tmon+1,$tmday,$thour,$tmin);
				$s_mes .= "���o�� ($tdate)";
				if(-f "$userdir/$id/depot_watch.cgi"){
					open my $wfh, ">> $userdir/$id/depot_watch.cgi";
					print $wfh "$s_mes<>$depot_line\n";
					close $wfh;
				}
				&penalty_depot($count);
	
				&add_log("���o", $l_mes);
	
				# ���o�����ݸނŐV�������т�����κڸ��݂ɒǉ�
				require './lib/add_collection.cgi';
				&add_collection;


#				Time::HiRes::sleep(2.5);
			}
			else {
				close $fh;
			}
		}
		&begin;
	}
}

#=================================================
# �a����
#=================================================
sub tp_200 {
	$mes .= '�ǂ��a���܂���?';

	my @menus = ('��߂�');
	push @menus, $m{wea} ? $weas[$m{wea}][1] : '';
	push @menus, $m{egg} ? $eggs[$m{egg}][1] : '';
	push @menus, $m{pet} > 0 ? $pets[$m{pet}][1] : '';
	push @menus, $m{gua} ? $guas[$m{gua}][1] : '';
	
	&menu(@menus);
	$m{tp} += 10;
}
sub tp_210 {
	return if &is_ng_cmd(1..4);

	my $line;
	if ($cmd eq '1' && $m{wea}) {
		# �����ŃI������p�Ɏ��f�[�^�����������Ă͂����Ȃ�
		# ���������ňӐ}���� return ����\��������
		$line = $m{wea_name} ? "$cmd<>32<>0<>0<>\n" : "$cmd<>$m{wea}<>$m{wea_c}<>$m{wea_lv}<>\n";
	}
	elsif ($cmd eq '2' && $m{egg}) {
		$line = "$cmd<>$m{egg}<>$m{egg_c}<>0<>\n";
	}
	elsif ($cmd eq '3' && $m{pet}) {
		$line = "$cmd<>$m{pet}<>$m{pet_c}<>0<>\n";
	}
	elsif ($cmd eq '4' && $m{gua}) {
		$line = "$cmd<>$m{gua}<>0<>0<>\n";
	}
	else {
		&begin;
		return;
	}
	
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_file���J���܂���");
	eval { flock $fh, 2; };
	push @lines, $_ while <$fh>;
	
	if (@lines >= $max_depot) {
		close $fh;
		$mes .= '����ȏ�a���邱�Ƃ��ł��܂���<br>';
		$m{is_full} = 1;
	}
	else {
		my $l_mes = "";
		push @lines, $line;
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
		
		if ($cmd eq '1') {
			if($m{wea_name}){
				$m{wea} = 32;
				$mes .= "������̎�𗣂ꂽ�r�[$m{wea_name}�͂�����$weas[$m{wea}][1]�ɂȂ��Ă��܂���<br>";
				$m{wea_name} = "";
			}
			$mes .= "$weas[$m{wea}][1]��a���܂���<br>";
			$l_mes = "$weas[$m{wea}][1]";
			$m{wea} = $m{wea_c} = $m{wea_lv} = 0;
		}
		elsif ($cmd eq '2') {
			$mes .= "$eggs[$m{egg}][1]��a���܂���<br>";
			$l_mes = "$eggs[$m{egg}][1]";
			$m{egg} = $m{egg_c} = 0;
		}
		elsif ($cmd eq '3') {
			$mes .= "$pets[$m{pet}][1]��$m{pet_c}��a���܂���<br>";
			$l_mes = "$pets[$m{pet}][1]��$m{pet_c}";
			&remove_pet;
		}
		elsif ($cmd eq '4') {
			$mes .= "$guas[$m{gua}][1]��a���܂���<br>";
			$l_mes = "$guas[$m{gua}][1]";
			$m{gua} = 0;
		}
		
		$m{is_full} = 1 if @lines >= $max_depot;

		&add_log("�a��", $l_mes);
	}
	&begin;
}

#=================================================
# ����
#=================================================
sub tp_300 {
	my @lines = ();
	my @sub_lines = ();
	my $count = 0;
	my $n_egg = 0;
	my $n_man = 0;
	my $n_hero = 0;	
	open my $fh, "+< $this_file" or &error("$this_file���J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>){
		++$count;
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
		if($kind == 2 && $item_no == 53){
			$line = "2<>42<>$item_c<>$item_lv<>\n";
			$n_egg++;
		}
		if($kind == 3 && $item_no == 180){
			$line = "3<>76<>$item_c<>$item_lv<>\n";
			$n_man++;
		}
		if($kind == 3 && $item_no == 181){
			$line = "3<>77<>$item_c<>$item_lv<>\n";
			$n_hero++;
		}
		push @lines, $line if $count <= $lost_depot; # �C��؂菈��
	}
	@lines = map { $_->[0] }
				sort { $a->[1] <=> $b->[1] || $a->[2] <=> $b->[2] }
					map { [$_, split /<>/ ] } @lines;
	while($n_egg>0 || $n_man>0 || $n_hero>0){
		my $line_i = rand(@lines);
		my $o_line = $lines[$line_i];
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $o_line;
		if($kind == 2 && $item_no == 42 && $n_egg > 0){
			$o_line = "2<>53<>$item_c<>$item_lv<>\n";
			$n_egg--;
		}
		if($kind == 3 && $item_no == 76 && $n_man > 0){
			$o_line = "3<>180<>$item_c<>$item_lv<>\n";
			$n_man--;
		}
		if($kind == 3 && $item_no == 77 && $n_hero > 0){
			$o_line = "3<>181<>$item_c<>$item_lv<>\n";
			$n_hero--;
		}
		$lines[$line_i] = $o_line;
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	$mes .= "�a���Ă�����̂𐮗����܂���<br>";
	&begin;
}

#=================================================
# ����ɑ���
#=================================================
sub tp_400 {
	$layout = 1;
	$mes .= "�N�ɉ��𑗂�܂���?<br>�����萔���F$need_money G<br>���O�萔���F$need_money_other G<br>";
	$mes .= '�����𑗂�ꍇ�͋��z����͂��Ă�������<br>';

	$mes .= qq|<form method="$method" action="$script"><p>���M��F<input type="text" name="send_name" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="cmd" value="0" checked>��߂�<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1">[$weas[$m{wea}][2]]$weas[$m{wea}][1]��$m{wea_lv}($m{wea_c}/$weas[$m{wea}][4])<br>| if $m{wea};
	$mes .= qq|<input type="radio" name="cmd" value="2">[��]$eggs[$m{egg}][1]($m{egg_c}/$eggs[$m{egg}][2])<br>| if $m{egg};
	$mes .= qq|<input type="radio" name="cmd" value="3">[�y]$pets[$m{pet}][1]��$m{pet_c}<br>| if $m{pet} > 0;
	$mes .= qq|<input type="radio" name="cmd" value="4">[$guas[$m{gua}][2]]$guas[$m{gua}][1]<br>| if $m{gua};
	$mes .= qq|<input type="radio" name="cmd" value="5">����<input type="text" name="send_money" value="0" class="text_box1" style="text-align:right">G<br>| if $m{money} > 0;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="����" class="button1"></p></form>|;
	
	$m{tp} += 10;
}
sub tp_410 {
	return if &is_ng_cmd(1..5);
	if ($m{shogo} eq $shogos[1][0]) {
		$mes .= "$shogos[1][0]�̕��͑��邱�Ƃ��ł��܂���<br>";
		&begin;
		return;
	}
	elsif ($in{send_name} eq '') {
		$mes .= '����悪�L������Ă��܂���<br>';
		&begin;
		return;
	}
	elsif ($m{sedai} <= 1 && $m{lv} < $need_lv) {
		$mes .= "1����ڂ�����$need_lv�����̐l�͑��邱�Ƃ��ł��܂���<br>";
		&begin;
		return;
	}
	elsif ($cmd eq '1' && $m{wea_name}) {
		$mes .= "�B�ꖳ��̕���𑗂邱�Ƃ͂ł��܂���<br>";
		&begin;
		return;
	}

	my $send_id = unpack 'H*', $in{send_name};
	my %datas = &get_you_datas($send_id, 1);
	
	# �����̏�����ς���Ƃ��납��
	if ($datas{is_full} && $cmd ne '5' && !&is_sabakan) {
		$mes .= "$in{send_name}�̗a���菊�����t�ő��邱�Ƃ��ł��܂���<br>";
		&begin;
		return;
	}
	
	my $pay = $datas{country} eq $m{country} ? $need_money : $need_money_other;
	
	if ($m{money} < $pay) {
		$mes .= "�X���萔��( $pay G)������܂���<br>";
		&begin;
		return;
	}

	my @kinds = ('', 'wea', 'egg', 'pet', 'gua');
	for my $taboo_item (@{ $taboo_items{ $kinds[$cmd] } }) {
		if ($taboo_item eq $m{ $kinds[$cmd] }) {
			my $t_item_name = $cmd eq '1' ? $weas[$m{wea}][1]
							: $cmd eq '2' ? $eggs[$m{egg}][1]
							: $cmd eq '3' ? $pets[$m{pet}][1]
							:               $guas[$m{gua}][1]
							;
			$mes .= "$t_item_name�͑��̐l�ɑ��邱�Ƃ͂ł��܂���<br>";
			&begin;
			return;
		}
	}
	
	my %lock = &get_lock_item;
	my $check_line = $cmd eq '1' ? "$cmd<>$m{wea}<>"
					: $cmd eq '2' ? "$cmd<>$m{egg}<>"
					: $cmd eq '3' ? "$cmd<>$m{pet}<>"
					:               "$cmd<>$m{gua}<>"
					;
	if ($lock{$check_line}) {
			$mes .= "���b�N����Ă���A�C�e���͑��̐l�ɑ��邱�Ƃ͂ł��܂���<br>";
			&begin;
			return;
	}
	
	if ($cmd eq '1' && $m{wea}) {
		&send_item($in{send_name}, $cmd, $m{wea}, $m{wea_c}, $m{wea_lv}, &is_sabakan);
		&mes_and_send_news("$in{send_name}��$weas[$m{wea}][1]�𑗂�܂���");
		$m{wea} = $m{wea_c} = $m{wea_lv} = 0;
		$m{money} -= $pay;
	}
	elsif ($cmd eq '2' && $m{egg}) {
		&send_item($in{send_name}, $cmd, $m{egg}, $m{egg_c}, 0, &is_sabakan);
		&mes_and_send_news("$in{send_name}��$eggs[$m{egg}][1]�𑗂�܂���");
		$m{egg} = $m{egg_c} = 0;
		$m{money} -= $pay;
	}
	elsif ($cmd eq '3' && $m{pet}) {
		&send_item($in{send_name}, $cmd, $m{pet}, $m{pet_c}, 0, &is_sabakan);
		&mes_and_send_news("$in{send_name}��$pets[$m{pet}][1]��$m{pet_c}�𑗂�܂���");
		&remove_pet;
		$m{money} -= $pay;
	}
	elsif ($cmd eq '4' && $m{gua}) {
		&send_item($in{send_name}, $cmd, $m{gua}, 0, 0, &is_sabakan);
		&mes_and_send_news("$in{send_name}��$guas[$m{gua}][1]�𑗂�܂���");
		$m{gua} = 0;
		$m{money} -= $pay;
	}
	elsif ($cmd eq '5' && $in{send_money} > 0 && $in{send_money} !~ /[^0-9]/) {
		if ($m{money} + $pay > $in{send_money}) {
			&send_money($in{send_name}, $m{name}, $in{send_money});
			&mes_and_send_news("$in{send_name}�� $in{send_money} G�𑗂�܂���");
			$m{money} -= $in{send_money} + $pay;
		}
		else {
			$mes .= "�萔������܂߂Ă���������܂���<br>";
		}
	}
	&begin;
}

#=================================================
# �ެݸ����߂ɔ���
#=================================================
sub tp_500 {
	$layout = 2;
	my($count, $sub_mes) = &checkbox_my_depot;

	my $lost_mes = '';
	my $lost_count = ($count - $lost_depot) < 0 ? 0 : $count - $lost_depot;
	$lost_mes = qq| / <font color="#FF0000">$lost_count</font>| if $lost_count;
	$count -= $lost_count;
	$mes .= "�ǂ�𔄂�܂���? [ $count / $max_depot$lost_mes ]<br>";
#	$mes .= "�ǂ�𔄂�܂���?[ $count / $max_depot ]<br>";
	$mes .= $sub_mes;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="����" class="button1"></p></form>|;

	$m{tp} += 10;
}
sub tp_510 {
	if ($in{uncheck_flag}) {
		$m{tp} -= 10;
		&{ 'tp_'. $m{tp} };
		return;
	}
	my($maxcount, $sub_mes) = &checkbox_my_depot;
	my $count = 0;
	my $is_rewrite = 0;
	my @junk = ();
	my @junk_log = ();
	my @depot_log = ();
	my %lock = &get_lock_item;
	open my $fh, "+< $this_file" or &error("$this_file���J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		++$count;
		if ($in{$count} eq '1') {
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
			if ($count <= $lost_depot && $lock{"$kind<>$item_no<>"}) {
				push @lines, $line;
			} else { # �C��؂�Ώۂ̱��т̓��b�N����
				$is_rewrite = 1;

				# �߯Ă��������ǋL ���͖��O����
				my $l_mes = &get_item_name($kind, $item_no, $item_c);
				push @depot_log, "$l_mes";
				$mes .= "$l_mes�𔄂�܂���<br>";
				$item_c = 0 if $kind eq '3'; # �ެݸ���߯Ă𗬂����̓��x����������
				$m{money} += $sall_price;

				# ��ʂɈꊇ���p����Ƃ��̐�����̧�ٵ���݂���̂�1��ōςނ悤�ɕύX
#				if (rand(2) < 1) {
					push @junk, "$kind<>$item_no<>$item_c<>\n";
#				}
				push @junk_log, "$kind<>$item_no<>$item_c<>$m{name}<>$time<>0<>\n";
				&penalty_depot($maxcount);
			}
		}
		else {
			push @lines, $line;
		}
	}
	if ($is_rewrite) {
		# �����̑q�ɂ̏�������
		seek  $fh, 0, 0;
		truncate $fh, 0; 
		print $fh @lines;
		close $fh;

		# �ެݸ�ɏ�������
		open my $fh2, ">> $logdir/junk_shop.cgi" or &error("$logdir/junk_shop.cgi̧�ق��J���܂���");
		print $fh2 @junk;
		close $fh2;

		# �ެݸ۸ނɏ�������
		open my $fh3, ">> $logdir/junk_shop_sub.cgi" or &error("$logdir/junk_shop_sub.cgi̧�ق��J���܂���");
		print $fh3 @junk_log;
		close $fh3;
	}
	else {
		close $fh;
	}

	if ($is_rewrite) { # �J��Ԃ��ɂȂ邪�Aflock����flock��������邽��
		&add_log("���p", @depot_log);
		&run_tutorial_quest('tutorial_junk_shop_sell_1');
	}

	&begin;
}

#=================================================
# �̂Ă�
#=================================================
sub tp_600 {
	$layout = 2;
	my($count, $sub_mes) = &radio_my_depot(0, 1);

	my $lost_mes = '';
	my $lost_count = ($count - $lost_depot) < 0 ? 0 : $count - $lost_depot;
	$lost_mes = qq| / <font color="#FF0000">$lost_count</font>| if $lost_count;
	$count -= $lost_count;
	$mes .= "�ǂ���̂Ă܂���? [ $count / $max_depot$lost_mes ]<br>";
#	$mes .= "�ǂ���̂Ă܂���?[ $count / $max_depot ]<br>";
	$mes .= $sub_mes;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�̂Ă�" class="button1"></p></form>|;

	$m{tp} += 10;
}
sub tp_610 {
	my($maxcount, $sub_mes) = &radio_my_depot(0, 1);
	my $count = 0;
	my $is_rewrite = 0;
	my %lock = &get_lock_item;
	my $l_mes = "";
	open my $fh, "+< $this_file" or &error("$this_file���J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		++$count;
		if ($cmd eq $count) {
			my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
			if ($count <= $lost_depot && $lock{"$kind<>$item_no<>"}) {
				push @lines, $line;
			} else { # �C��؂�Ώۂ̱��т̓��b�N����
				$is_rewrite = 1;

				# �߯Ă��������ǋL ���͖��O����
				$l_mes = &get_item_name($kind, $item_no, $item_c);
				$mes .= "$l_mes���̂Ă܂���<br>";
			}
		}
		else {
			push @lines, $line;
		}
	}
	if ($is_rewrite) {
		seek  $fh, 0, 0;
		truncate $fh, 0; 
		print $fh @lines;
	}
	close $fh;
	&add_log("�j��", $l_mes) if $is_rewrite;
	&begin;
}

#=================================================
# ���b�N
#=================================================
sub tp_700 {
	$layout = 2;
	my($count, $sub_mes) = &checkbox_my_depot_lock_checked;

	my $lost_mes = '';
	my $lost_count = ($count - $lost_depot) < 0 ? 0 : $count - $lost_depot;
	$lost_mes = qq| / <font color="#FF0000">$lost_count</font>| if $lost_count;
	$count -= $lost_count;
	$mes .= "�ǂ�����b�N���܂���? [ $count / $max_depot$lost_mes ]<br>";
#	$mes .= "�ǂ�����b�N���܂���?[ $count / $max_depot ]<br>";
	$mes .= $sub_mes;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���b�N" class="button1"></p></form>|;

	$m{tp} += 10;
}
sub tp_710 {
	if ($in{uncheck_flag}) {
		$m{tp} -= 10;
		&{ 'tp_'. $m{tp} };
		return;
	}

	my %lock = (); # ���b�N���

	# �q�ɓ��ɑ��݂��Ȃ��̂��A�����b�N�����̂��̔��f���ł��Ȃ��ƃA�����b�N�ł��Ȃ���ԂɂȂ肤��
	# �q�ɓ��Ń��b�N�w�聨�ȑO���烍�b�N�����b�N�i�������j
	# �q�ɓ��ɑ��݂��Ȃ����ȑO���烍�b�N�����b�N�i�ꌩ���������A�����b�N�Ɣ��ʂ��Ȃ��ƃA�����b�N���Ă�����Ȃ��j
	# �q�ɓ��ŃA�����b�N�w�聨�ȑO���烍�b�N���A�����b�N�i�������j

	# ���b�N�w�肳�ꂽ�A�C�e���̎擾
	open my $fh, "< $this_file" or &error("$this_file���J���܂���");
	while (my $line = <$fh>) {
		++$count;
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
		if ($in{$count} eq '1' && $lock{"$kind<>$item_no<>"} == 0) {
			$lock{"$kind<>$item_no<>"} = 1; # ���b�N
		}
		elsif ($in{$count} == 0 && $lock{"$kind<>$item_no<>"} == 0) {
			$lock{"$kind<>$item_no<>"} = -1; # �A�����b�N
		}
		# �q�ɓ��ɑ��݂��Ȃ��A�C�e���ɂ��Ă͏]���̃��b�N���𗘗p��
	}
	close $fh;

	# �]���̃��b�N�����擾���X�V
	open my $lfh, "+< $this_lock_file" or &error("$this_lock_file���J���܂���");
	eval { flock $lfh, 2; };
	while (my $line = <$lfh>){
		chomp $line;
		$lock{$line} = 1 if $lock{$line} > -1; # �A�����b�N�w�肳��ĂȂ��Ȃ�����������b�N
	}

	seek  $lfh, 0, 0;
	truncate $lfh, 0;
	foreach my $line(keys(%lock)){
		if ($lock{$line} > 0) {
			print $lfh "$line\n";
		}
	}
	close $lfh;
	&begin;
}

#=================================================
# ����
#=================================================
sub tp_800 {
	if (-f "$this_log") {
		my @lines = ();
		open my $fh, "< $this_log" or &error("$this_log���J���܂���");
		while (my $line = <$fh>){
			$mes .= "$line<br>";
		}
		close $fh;
	}
	&begin;
}

#=================================================
# ��������
#=================================================
sub penalty_depot {
	my $count = shift;
	return if $count eq '';

	if ($count > $max_depot) {
		$m{is_full} = 1;
		$mes .= "���� $penalty_money G���x�����܂���<br>";
		$m{money} -= $penalty_money;
	}
	else {
		$m{is_full} = 0;
	}
}


#=================================================
# <input type="radio" �t�̗a���菊�̕�
#=================================================
sub radio_my_depot {
	my $no = shift; # �I����Ԃɂ��鱲�єԍ� 0 �Łu��߂�v
	my $is_show = shift; # ���Ă��鱲�Â�\�����邩�ǂ���
	my $count = 0;
	my %lock = &get_lock_item;
	my $sub_mes = qq|<form method="$method" action="$script">|;
	my $checked = " checked" unless $no;
	$sub_mes .= qq|<label><input type="radio" name="cmd" value="0"$checked>��߂�</label><br>|;
	open my $fh, "< $this_file" or &error("$this_file ���ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		++$count;
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
		if (!$is_show && $count > $lost_depot) {
			my $item_name = &get_item_name($kind, $item_no, $item_c, $item_lv);
			$sub_mes .= &show_item_datas($item_name, $lock{"$kind<>$item_no<>"}, $lost_depot < $count);
		}
		else {
			$checked = $no == $count ? " checked" : "" ;
			$sub_mes .= qq|<label>| unless $is_mobile;
			$sub_mes .= qq|<input type="radio" name="cmd" value="$count"$checked>|;
			my $item_name = &get_item_name($kind, $item_no, $item_c, $item_lv);
			$sub_mes .= &show_item_datas($item_name, $lock{"$kind<>$item_no<>"}, $lost_depot < $count);
			$sub_mes .= qq|</label>| unless $is_mobile;
			$sub_mes .= qq|<br>|;
		}
	}
	close $fh;

	$m{is_full} = $count >= $max_depot ? 1 : 0;

	return $count, $sub_mes;
}

#=================================================
# <input type="checkbox" �t�̗a���菊�̕�
#=================================================
sub checkbox_my_depot {
	my $count = 0;
	my $sub_mes = "";
	my %lock = &get_lock_item;
	if ($is_mobile) {
		$sub_mes .= qq|<form method="$method" action="$script">|;
		$sub_mes .= qq|<input type="hidden" name="uncheck_flag" value="1">|;
		$sub_mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$sub_mes .= qq|<p><input type="submit" value="�`�F�b�N���O��" class="button1"></p></form>|;
	}
	$sub_mes .= qq|<form method="$method" action="$script">|;
	if (!$is_mobile) {
		$sub_mes .= qq|<input type="button" name="all_unchecked" value="�`�F�b�N���O��" class="button1" onclick="\$('input:checkbox').prop('checked',false); "><br>|;
	}
	open my $fh, "< $this_file" or &error("$this_file ���ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		++$count;
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
		$sub_mes .= qq|<label>| unless $is_mobile;
		$sub_mes .= qq|<input type="checkbox" name="$count" value="1">|;
		my $item_name = &get_item_name($kind, $item_no, $item_c, $item_lv);
		$sub_mes .= &show_item_datas($item_name, $lock{"$kind<>$item_no<>"}, $lost_depot < $count);
		$sub_mes .= qq|</label>| unless $is_mobile;
		$sub_mes .= qq|<br>|;
	}
	close $fh;
	
	$m{is_full} = $count >= $max_depot ? 1 : 0;
	
	return $count, $sub_mes;
}

#=================================================
# <input type="checkbox" �t�̗a���菊�̕�
#=================================================
sub checkbox_my_depot_lock_checked {
	my $count = 0;
	my $sub_mes = "";
	my %lock = &get_lock_item;
	if ($is_mobile) {
		$sub_mes .= qq|<form method="$method" action="$script">|;
		$sub_mes .= qq|<input type="hidden" name="uncheck_flag" value="1">|;
		$sub_mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$sub_mes .= qq|<p><input type="submit" value="�`�F�b�N���O��" class="button1"></p></form>|;
	}
	$sub_mes .= qq|<form method="$method" action="$script">|;
	if (!$is_mobile) {
		$sub_mes .= qq|<input type="button" name="all_unchecked" value="�`�F�b�N���O��" class="button1" onclick="\$('input:checkbox').prop('checked',false); "><br>|;
	}
	my %sames = ();
	open my $fh, "< $this_file" or &error("$this_file ���ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		++$count;
		my($kind, $item_no, $item_c, $item_lv) = split /<>/, $line;
		# �d������A�C�e���͍ŏ��̈�ڂ����\��
		unless ($sames{"$kind<>$item_no<>"}) {
			$sub_mes .= qq|<label>| unless $is_mobile;
			$sub_mes .= qq|<input type="checkbox" name="$count" value="1"|;
			$sub_mes .= qq| checked| if $lock{"$kind<>$item_no<>"};
			$sub_mes .= qq|>|;
			my $item_name = &get_item_name($kind, $item_no, $item_c, $item_lv);
			$sub_mes .= &show_item_datas($item_name, $lock{"$kind<>$item_no<>"}, $lost_depot < $count);
			$sub_mes .= qq|</label>| unless $is_mobile;
			$sub_mes .= qq|<br>|;
		}
		$sames{"$kind<>$item_no<>"}++;
	}
	close $fh;
	
	$m{is_full} = $count >= $max_depot ? 1 : 0;
	
	return $count, $sub_mes;
}

#=================================================
# ���b�N�A�C�e���̎擾
#=================================================
sub get_lock_item {
	my %lock = ();
	open my $lfh, "< $this_lock_file" or &error("$this_lock_file���J���܂���");
	while (my $line = <$lfh>){
		chomp $line;
		$lock{$line}++;
	}
	close $lfh;

	return %lock;
}

#=================================================
# �q��۸�
# add_log("����܂���", "item1"[, "item2", "item3"])
#=================================================
sub add_log {
	my $type = shift;
	my @items = @_;

	my($tmin,$thour,$tmday,$tmon,$tyear) = (localtime($time))[1..4];
	$tdate = sprintf("%d/%d %02d:%02d", $tmon+1,$tmday,$thour,$tmin);
	my $s_mes = "";
	for my $item (@items) {
		$s_mes .= "$item";
		$s_mes .= "," if @items > 1;
	}
	$s_mes = substr($s_mes, 0,  -1) if @items > 1;
	$s_mes .= "��$type($tdate)";

	if (-f $this_log) {
		open my $wfh, "+< $this_log";
		eval { flock $wfh, 2; };
		my @log_lines = ();
		my $log_count = 0;
		while (my $log_line = <$wfh>){ 
			push @log_lines, $log_line;
			$log_count++;
			last if $log_count > 30;
		}
		unshift @log_lines, "$s_mes\n";
		seek  $wfh, 0, 0;
		truncate $wfh, 0;
		print $wfh @log_lines;
		close $wfh;
	}
	else {
		open my $wfh, "> $this_log";
		print $wfh "$s_mes\n";
		close $wfh;
	}
}

#=================================================
# �A�C�e���f�[�^�̕\��
#=================================================
sub show_item_datas {
	my ($item_name, $is_lock, $is_over) = @_;
	my $item_datas = '';
	$item_datas .= $item_name;
	$item_datas .= qq|<img src="$icondir/emoji/1f512.png" width="14px" height="14px">| if $is_lock;
	$item_datas .= ' ���Ă܂�' if $is_over;
	return $item_datas;
}

1; # �폜�s��

require "$datadir/hunting.cgi";
#=================================================
# ���� Created by Merino
#=================================================

# ���яE���m��(����1)
my $get_item_par = 200;

# ���{�X���������o�Ă���m��(����1)
my $boss_par = $pets[$m{pet}][2] eq 'hunt_lv' ? 5:
				$pets[$m{pet}][2] eq 'no_boss' ? 100:
				20;

# �͂��ꃁ�^�����o�Ă���m��(����1)
my $metal_par = $pets[$m{pet}][2] eq 'no_boss' ? (50-2*$m{pet_c}) :50;

# �{�X��������m��(����1)
# ���O�C���������𑱂��邱�ƂŃ{�X����K��������ꂽ �������ǂ�������ɓ���������
# ����������Ɠ������グ�Ă��ǂ���������Ȃ����A����Ƃ͂܂��ʌ����ްŽ�ݽ�����o�Ă��Ȃ���Ԃ������̂��C��
# �޽���ȒP�ɓ����������ްŽ�ݽ����肪���₷���Ȃ��Ă�����̂ł�����Ƃ���
my $boss_run_away = 40; # ���� 50

# ���ʂ�NPC�����X�^�[���o��m��(����1)
my $npc_par = 5;

# ���{�X�����{�[�i�X
my @bonus = (
	['weapon', 33, 0, 0], # л��
	['money', 1000000, 0, 0],
	['money', 500000, 0, 0],
	['money', 100000, 0, 0],
	['money', 50000, 0, 0],
	['money', 10000, 0, 0],
	['money', 5000, 0, 0],
);

my @no_boss_eggs = (4..29);

# �V���P�������p�\����
my $new_sedai = 5;

#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if ($m{tp} <= 1 && $m{hp} < 10) {
		$mes .= "��������̂�$e2j{hp}�����Ȃ����܂�<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	elsif (&is_act_satisfy) { # ��J���Ă���ꍇ�͍s���Ȃ�
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	$m{turn} = 0;
	$m{tp} = 1 if $m{tp} > 1;
	$mes .= '�����𓢔����ɍs���܂�<br>';
	$mes .= '�ǂ��Ɍ������܂���?<br>';
	
	my $m_st = &m_st;
	my @menus = ('��߂�');
	for my $i (0..$#places) {
		next if $i == 0 && $m{sedai} > $new_sedai;
		push @menus, "$places[$i][2]" if $m_st * 2 >= $places[$i][1] || $pets[$m{pet}][2] eq 'hunt_lv';
	}

	&menu(@menus);
}
sub tp_1 {
	if ($cmd) {
		$m{stock} = $cmd-1;
		$m{stock}++ if $m{sedai} > $new_sedai;
		&_get_hunt_you_data;
	}
	else {
		$mes .= '��߂܂���<br>';
		&begin;
	}
}

#=================================================
# Get ����f�[�^
#=================================================
sub _get_hunt_you_data {
	my $line = '';
	# ['boss',	999999,	'�N�̋�̒�',	[2,3,38,40,41],],
	my $data_num = $places[$m{stock}][0]; # �N�̋�̒낾�� $data_num �� 'boss' �ɂȂ�

	if (-f "$datadir/metal.cgi" && (!$m{no_boss} || $data_num eq 'boss') && 5 < $m{stock} && rand($metal_par) < 1) { # �ްŽ�ݽ��
		require "$datadir/metal.cgi";
		for my $k (qw/name country max_hp max_mp at df mat mdf ag cha wea skills mes_win mes_lose icon wea_name/) {
			$y{$k} = $metal[$m{stock}]{$k};
		}
		$y{icon} = $default_icon unless -f "$icondir/$y{icon}"; # $y{icon} = &random_icon;
		$m{tp} = 500;
		$mes .= "�{�[�i�X�����X�^�[ $y{name} �ɑ��������I<br>";
		&n_menu;
	}
	elsif ($data_num eq 'boss' || (!$m{no_boss} && 5 < $m{stock} && rand($boss_par) < 1 && -f "$logdir/monster/boss.cgi")) { # �޽�ݽ��
		open my $bfh, "< $logdir/monster/boss.cgi" or &error("$logdir/monster/boss.cgi̧�ق�����܂���");
		$line = <$bfh>;
		close $bfh;
		my @datas = split /<>/, $line;
		my $i = 0;
		for my $k (qw/name country max_hp max_mp at df mat mdf ag cha wea skills mes_win mes_lose icon wea_name/) {
			$y{$k} = $datas[$i];
			++$i;
		}
		$y{icon} = $default_icon unless -f "$icondir/$y{icon}"; # $y{icon} = &random_icon;
		if ( rand($m{cha}) < rand(2000) ) {
			$m{tp} = 400;
			$mes .= "���{�X $y{name} ���P���������Ă��܂���<br>";
			&n_menu;
		}
		else {
			$m{tp} = 300;
			$mes .= "���{�X $y{name} �����܂�<br>";
			&menu('�키','������');
		}
	}
	elsif (rand($npc_par) < 1) { # NPC�ݽ��
		require "$datadir/npc_hunting.cgi";
		my $stock_npcs_ref = $npc[$m{stock}];
		my @stock_npcs = @$stock_npcs_ref;
		my $enemy = int(rand($stock_npcs));
		for my $k (qw/name country max_hp max_mp at df mat mdf ag cha wea skills mes_win mes_lose icon wea_name/) {
			$y{$k} = $stock_npcs[$enemy]{$k};
		}
		if ( rand($m{cha}) < rand($y{cha}) ) {
			$m{tp} = 200;
			$mes .= "$y{name} ���P���������Ă��܂���<br>";
			&n_menu;
		}
		else {
			$m{tp} = 100;
			$mes .= "$y{name} �����܂�<br>";
			&menu('�키','������');
		}
	}
	else { # �ݽ��
		open my $fh, "< $logdir/monster/$data_num.cgi" or &error("$logdir/monster/$data_num.cgi̧�ق�����܂���");
		# $. �ǂݍ��񂾍s���������������Ă��� 1�s�ڂ͕K���������A����ȍ~�̍s�ɂ��Ă͊m�� �o�ė����ݽ���΂��Ă��������ǁA���Ȃ�G�N�Z�����g�ȃR�[�h
		rand($.) < 1 and $line = $_ while <$fh>;
		close $fh;

		my @datas = split /<>/, $line;
		my $i = 0;
		for my $k (qw/name country max_hp max_mp at df mat mdf ag cha wea skills mes_win mes_lose icon wea_name/) {
			$y{$k} = $datas[$i];
			++$i;
		}
		$y{icon} = $default_icon unless -f "$icondir/$y{icon}";
		$y{wea_name} = '';
		if ( rand($m{cha}) < rand($y{cha}) ) {
			$m{tp} = 200;
			$mes .= "$y{name} ���P���������Ă��܂���<br>";
			&n_menu;
		}
		else {
			$m{tp} = 100;
			$mes .= "$y{name} �����܂�<br>";
			&menu('�키','������');
		}
	}

	$y{hp} = $y{max_hp};
	$y{mp} = $y{max_mp};
	$y{gua} = 0;
}

#=================================================
# �키 or ������
#=================================================
sub tp_100 {
	if ($cmd eq '0') {
		$mes .= "$y{name} �Ɛ킢�܂�<br>";
		$m{tp} = 200;
		&n_menu;
	}
	elsif ( rand($m{ag}) > rand($y{ag}) ) {
		$mes .= '�����܂���<br>';
		&begin;
	}
	else {
		$mes .= '�������܂���ł����B�퓬�Ԑ��ɓ���܂�<br>';
		$m{tp} = 200;
		&n_menu;
	}
}

#=================================================
# �퓬
#=================================================
sub tp_200 {
	require './lib/hunting_battle.cgi';

	# ����
	if ($m{hp} <= 0) {
		if($m{stock} == 0){
			$m{act} += 8;
		}else {
			my $lossp = $m{stock} >= 5 ? 0.1:
					$m{stock} == 4 ? 0.08:
					$m{stock} > 1 ? 0.05:
					0.01;
	   		my $vloss = $m{money} < 0 ? 10000 :int($m{money} * $lossp);
	   		$m{money} -= $vloss;
			$mes .= "$vloss G�������܂���<br>";
			$m{act} += 12;
		}

		&run_tutorial_quest('tutorial_hunting_1');

		&refresh;
		&n_menu;
		
	}
	# ����
	elsif ($y{hp} <= 0) {
		# İ�ٽð������������҂��ƌo���l���Ȃ�
		my $y_st = &y_st;
		my $st_lv = &st_lv($y_st);
		my $v = $st_lv eq '2' ? int( rand(10) + 10) 
			  : $st_lv eq '0' ? int( rand(3)  + 1)
			  :                 int( rand(5)  + 5)
			  ;
		$v = int( rand(10) + 10) if $m{stock} == 0;
		my $vv = int( $m{stock} * 70 + $y_st * 0.1);
		
		&c_up('tou_c');
		$v  = &use_pet('hunting', $v);
		$vv = &use_pet('hunt_money', $vv);
		$vv *= 1.5 if $m{master_c} eq 'tou_c';
		$m{exp} += $v;
		$m{act} += 6;
		if($m{stock} == 0){
			$m{egg_c} += 1 if $m{egg};
		}elsif($m{no_boss}){
			$m{egg_c} += int(rand($m{stock}-1)) if $m{egg};
		}else{
			$m{egg_c} += int(rand($m{stock}-1)+$m{stock}) if $m{egg};
		}
		$m{money} += $vv;
		$mes .= "$v ��$e2j{exp}�� $vv G����ɓ���܂���<br>";
		
		# ���ѹޯ�(�����߯ĐE�Ƃ��Ǝ擾��up)
		$get_item_par *= 0.4 if $pets[$m{pet}][2] eq 'get_item' || $jobs[$m{job}][1] eq '�V�ѐl' || $m{master_c} eq 'tou_c';
		$get_item_par = 400 if $m{stock} == 0;
		$get_item_par = 1000 if $m{no_boss};
		&_get_item if int(rand($get_item_par)) == 0;
		
		if ($w{world} eq $#world_states-4) {
			require './lib/fate.cgi';
			&super_attack('hunting');
		}
		
		$mes .= '�����𑱂��܂���?<br>';
		&menu('������','��߂�','�����n�ύX');

		&run_tutorial_quest('tutorial_hunting_1');

		$m{tp} += 10;
	}
}

#=================================================
# �p�� or ��߂�
#=================================================
sub tp_210 {
	if ($cmd eq '0') {
		&_get_hunt_you_data;
	}elsif ($cmd eq '2') {
		&begin;
	}else {
		$mes .= '�������I�����܂�<br>';
		&refresh;
		&n_menu;
	}
}

#=================================================
# �키 or ������(���{�X)
#=================================================
sub tp_300 {
	if ($cmd eq '0') {
		$mes .= "$y{name} �Ɛ킢�܂�<br>";
		$m{tp} = 400;
		&n_menu;
	}
	elsif ( rand($m{ag}) > rand(2000) ) {
		$mes .= '�����܂���<br>';
		&begin;
	}
	else {
		$mes .= '�������܂���ł����B�퓬�Ԑ��ɓ���܂�<br>';
		$m{tp} = 400;
		&n_menu;
	}
}

#=================================================
# ���{�X�퓬
#=================================================
sub tp_400 {
	require './lib/boss_battle.cgi';

	# ����
	if ($m{hp} <= 0) {
		open my $bfh, "+< $logdir/monster/boss.cgi" or &error("$logdir/monster/boss.cgi̧�ق�����܂���");
		my $head_line = <$bfh>;
		my $is_added = 1;
		my @lines = ();
		push @lines, "$y{name}<>$y{country}<>$y{hp}<>$y{max_mp}<>$y{at}<>$y{df}<>$y{mat}<>$y{mdf}<>$y{ag}<>$y{cha}<>$y{wea}<>$y{skills}<>$y{mes_win}<>$y{mes_lose}<>$y{icon}<>$y{wea_name}<>\n";
		if($y{max_hp} > $y{hp}){
			while(my $line = <$bfh>){
				my($bname, $bdamage) = split /<>/, $line;
				if($bname eq $m{name}){
					$bdamage += $y{max_hp} - $y{hp};
					$is_added = 0;
				}
				push @lines, "$bname<>$bdamage<>\n";
			}
			if($is_added){
				my $bdamage = $y{max_hp} - $y{hp};
				push @lines, "$m{name}<>$bdamage<>\n";
			}
		}
		seek  $bfh, 0, 0;
		truncate $bfh, 0;
		print $bfh @lines;
		close $bfh;

		if ($m{stock} == 0) {
			$m{act} += 8;
		}
		else {
			my $lossp = $m{stock} >= 9 ? 0.5:
					$m{stock} >= 5 ? 0.1:
					$m{stock} == 4 ? 0.08:
					$m{stock} > 1 ? 0.05:
					0.01;
			if ($y{at} > 999999 && $m{stock} < 9) {
				$mes .= "���̃{�X�������̂�҂��ĂˁB<br>";
			} else {
		   		my $vloss = $m{money} < 0 ? 10000 :int($m{money} * $lossp);
		   		$m{money} -= $vloss;
				$mes .= "$vloss G�������܂���<br>";
				$m{act} += $m{stock} >= 9 ? 100 : 12;
			}
		}
		&refresh;
		&n_menu;
	}
	# ����
	elsif ($y{hp} <= 0) {
		&win_boss_bonus;
		
		# İ�ٽð������������҂��ƌo���l���Ȃ�
		my $y_st = &y_st;
		my $st_lv = &st_lv($y_st);
		my $v = $st_lv eq '2' ? int( rand(10) + 10) 
			  : $st_lv eq '0' ? int( rand(3)  + 1)
			  :                 int( rand(5)  + 5)
			  ;
		$v = int( rand(10) + 10) if $m{stock} == 0;
		my $vv = int( $m{stock} * 70 + $y_st * 0.1);
		
		&c_up('tou_c');
		$v  = &use_pet('hunting', $v);
		$vv = &use_pet('hunt_money', $vv);
		$m{exp} += $v;
		$m{act} += 6;
		if($m{stock} == 0){
			$m{egg_c} += 1 if $m{egg};
		}else{
			$m{egg_c} += int(rand($m{stock}-1)+$m{stock}) if $m{egg};
		}
		$m{money} += $vv;
		$mes .= "$v ��$e2j{exp}�� $vv G����ɓ���܂���<br>";
		
		# ���ѹޯ�(�����߯ĐE�Ƃ��Ǝ擾��up)
		$get_item_par *= 0.4 if $pets[$m{pet}][2] eq 'get_item' || $jobs[$m{job}][1] eq '�V�ѐl';
		$get_item_par = 400 if $m{stock} == 0;
		&_get_item if int(rand($get_item_par)) == 0;
		
		if ($w{world} eq $#world_states-4) {
			require './lib/fate.cgi';
			&super_attack('boss');
		}
		
		$mes .= '�����𑱂��܂���?<br>';
		&menu('������','��߂�','�����n�ύX');
		$m{tp} = 210;
	}
	elsif (defined($cmd) && rand($boss_run_away) < 1) {
		open my $bfh, "+< $logdir/monster/boss.cgi" or &error("$logdir/monster/boss.cgi̧�ق�����܂���");
		my $head_line = <$bfh>;
		my $is_added = 1;
		my @lines = ();
		push @lines, "$y{name}<>$y{country}<>$y{hp}<>$y{max_mp}<>$y{at}<>$y{df}<>$y{mat}<>$y{mdf}<>$y{ag}<>$y{cha}<>$y{wea}<>$y{skills}<>$y{mes_win}<>$y{mes_lose}<>$y{icon}<>$y{wea_name}<>\n";
		if ($y{max_hp} > $y{hp}) {
			while (my $line = <$bfh>) {
				my ($bname, $bdamage) = split /<>/, $line;
				if ($bname eq $m{name}) {
					$bdamage += $y{max_hp} - $y{hp};
					$is_added = 0;
				}
				push @lines, "$bname<>$bdamage<>\n";
			}
			if ($is_added) {
				my $bdamage = $y{max_hp} - $y{hp};
				push @lines, "$m{name}<>$bdamage<>\n";
			}
		}
		seek  $bfh, 0, 0;
		truncate $bfh, 0;
		print $bfh @lines;
		close $bfh;

		$m{act} += 8;
		$mes .= "$y{name}�u��ꂽ����A��B�^���悩�����ȁI�v<br>";
		&refresh;
		&n_menu;
	}
}

#=================================================
# �{�[�i�X�퓬
#=================================================
sub tp_500 {
	require './lib/bonus_battle.cgi';

	# ����
	if ($m{hp} <= 0) {
		if($m{stock} == 0){
			$m{act} += 8;
		}else {
			my $lossp =$m{stock} >= 9 ? 0.5:
					$m{stock} >= 5 ? 0.1:
					$m{stock} == 4 ? 0.08:
					$m{stock} > 1 ? 0.05:
					0.01;
	   		my $vloss = $m{money} < 0 ? 10000 :int($m{money} * $lossp);
	   		$m{money} -= $vloss;
			$mes .= "$vloss G�������܂���<br>";
			$m{act} += $m{stock} >= 9 ? 100 : 12;
		}
		&refresh;
		&n_menu;
	}
	# ����
	elsif ($y{hp} <= 0) {
		# İ�ٽð������������҂��ƌo���l���Ȃ�
		my $y_st = &y_st;
		my $st_lv = &st_lv($y_st);
		my $v = 30 * $m{stock};
		my $vv = int( $m{stock} * 70 + $y_st * 0.1);
		
		&c_up('tou_c');
		$v  = &use_pet('hunting', $v);
		$vv = &use_pet('hunt_money', $vv);
		$m{exp} += $v;
		$m{act} += 6;
		if($m{stock} == 0){
			$m{egg_c} += 1 if $m{egg};
		}else{
			$m{egg_c} += int(rand(25)) + int($m{stock} - 4) * 25 if $m{egg};
		}
		$m{money} += $vv;
		$mes .= "$v ��$e2j{exp}�� $vv G����ɓ���܂���<br>";
		
		# ���ѹޯ�(�����߯ĐE�Ƃ��Ǝ擾��up)
		$get_item_par = 80;
		&_get_item if int(rand($get_item_par)) == 0;
		
		$mes .= '�����𑱂��܂���?<br>';
		&menu('������','��߂�','�����n�ύX');
		$m{tp} = 210;
	}
}

#=================================================
# ����(�Ϻ�)�E������
#=================================================
sub _get_item {
	my @egg_nos = @{ $places[$m{stock}][3] };
	@egg_nos = @no_boss_eggs if $m{no_boss};
	my $egg_no = $egg_nos[int(rand(@egg_nos))];
	
	$mes .= qq|<font color="#FFCC00">$eggs[$egg_no][1]���E���܂���!</font><br>|;
	if ($m{is_full}) {
		$mes .= "�������A�a���菊�������ς��Ȃ̂�$eggs[$egg_no][1]��������߂܂���<br>";
	}
	else {
		$mes .="$eggs[$egg_no][1]��a���菊�ɑ���܂���!<br>";
		&send_item($m{name}, 2, $egg_no);
	}
}

#=================================================
# �K���ȃA�C�R����\��
#=================================================
sub random_icon {
	my $ricon;
	my @icons = ();
	opendir my $dh, "$icondir" or &error('�A�C�R���t�H���_���J���܂���');
	while(my $file_name = readdir $dh){
		next if $file_name =~ /^\./;
		next if $file_name =~ /\.html$/;
		next if $file_name =~ /\.db$/;
		
		push @icons, $file_name;
	}
	$ricon = @icons[int(rand(@icons))];
	if($ricon eq ''){
		$ricon = $default_icon;
	}
	return $ricon;
}
#=================================================
# ���{�X�ɏ���
#=================================================
sub win_boss_bonus {
	my $w_name = &name_link($m{name});
	if ($w{world} eq '16' || ($w{world} eq '19' && $w{world_sub} eq '16')) {
		$w_name = '������';
	}
	my $message = "<b>$m{name}�Ƃ��̒��Ԃ������{�X�����j���܂���</b>";
	$mes .= "$message<br>";
	&write_world_news("<b>$c_m��$w_name�Ƃ��̒��Ԃ������{�X�����j���܂���</b>", 1);
	&send_twitter("$c_m��$w_name�Ƃ��̒��Ԃ������{�X�����j���܂���");
#	&mes_and_world_news("", 1);

	open my $bfh, "+< $logdir/monster/boss.cgi" or &error("$logdir/monster/boss.cgi̧�ق�����܂���");
	my $head_line = <$bfh>;
	my @lines = ();
	my @attackers = ();
	push @lines, "�����C�x���g<>0<>999999999999<>999999999999<>99999999<>99999999<>99999999<>99999999<>99999999<>99999999<>32<>67,67,67,67,67<>���������C�x���g�����玟�̒��{�X�C�x���g��҂��Ă�<>�Ȃ����Ă���<>$default_icon<>�p���`�i���@�j<>\n";
	my $is_find = 0;
	while(my $line = <$bfh>){
		my($bname, $bdamage) = split /<>/, $line;
		if($bname eq $m{name}){
			$bdamage += $y{max_hp};
			$is_find = 1;
			push @attackers, "$m{name}<>$bdamage<>\n";
		}else{
			push @attackers, $line;
		}
	}
	seek  $bfh, 0, 0;
	truncate $bfh, 0;
	print $bfh @lines;
	close $bfh;
	
	unless($is_find){
		push @attackers, "$m{name}<>$y{max_hp}<>\n";
	}
	
	@attackers = reverse(map { $_->[0] }
				sort { $a->[2] <=> $b->[2] }
					map { [$_, split /<>/ ] } @attackers);
	my $rank = 0;
	my $debug_mes = '';
	for my $line (@attackers){
		my($bname, $bdamage) = split /<>/, $line;
		if($rank >= @bonus){
			&send_money($bname, "���{�X���j�v��", 1000);
		}else{
			if($bonus[$rank][0] eq 'money'){
				&send_money($bname, "���{�X���j�v��", $bonus[$rank][1]);
			}elsif($bonus[$rank][0] eq 'weapon'){
				&send_item($bname, 1, $bonus[$rank][1], $bonus[$rank][2], $bonus[$rank][3]);
			}elsif($bonus[$rank][0] eq 'egg'){
				&send_item($bname, 2, $bonus[$rank][1], $bonus[$rank][2], $bonus[$rank][3]);
			}elsif($bonus[$rank][0] eq 'pet'){
				&send_item($bname, 3, $bonus[$rank][1], $bonus[$rank][2], $bonus[$rank][3]);
			}
		}
		$rank++;
	}
}
1; # �폜�s��

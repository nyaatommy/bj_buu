#================================================
# ���C����� Created by Merino
#================================================

# ���X�̔�����̐ŋ�(0(�ŋ��Ȃ�)�`0.99�܂�)
my $shop_sale_tax = 0.2;
# �M���h�}�X�^�[�̐ŋ��Ə���(0(�ŋ��Ȃ�)�`0.99�܂�)
my $guild_master_tax_rate = 1.0;
# �����ȃM���h�̐ŋ��Ə���(0(�ŋ��Ȃ�)�`1.0�܂�)
my $guild_prior_tax_rate = 1.0;
# ���̑��̃M���h�̐ŋ��Ə���(0(�ŋ��Ȃ�)�`1.0�܂�)
my $guild_ferior_tax_rate = 1.0;

# �ƭ� ���ǉ�/�ύX/�폜/���בւ��\
my @menus = (
	['�X�V',		''],
	['�����ݸ�Ӱ�',	'shopping'],
	['�a���菊',	'depot'],
	['����',	'depot_country'],
	['ϲٰ�',		'myself'],
	['�C�s',		'training'],
	['����',		'hunting'],
	['�����',		'country'],
	['����',		'domestic'],
	['�O��',		'promise'],
	['�R��',		'military'],
	['�푈',		'war_form'],
);

if ($m{incubation_switch} && $m{egg} && $m{egg_c} >= $eggs[$m{egg}][2]) {
	push @menus, ['�z��', 'incubation'];
}
if (&on_summer) {
	push @menus, ['�čՂ�', 'summer_festival'];
}

#================================================
sub begin {
	&menu( map { $_->[0] } @menus );
	&main_system;
}
sub tp_1 { $cmd ? &b_menu(@menus) : &begin; }


#================================================
# Ҳݼ���
#================================================
sub main_system {
	# Lv up
	if ($m{exp} >= 100) {
		if ($m{egg}) {
			$m{egg_c} += int(rand(6)+10);
			$m{egg_c} += int(rand(16)+20) if $jobs[$m{job}][1] eq '���m';
			push @menus, ['�z��', 'incubation'] if ($m{incubation_switch} && $m{egg} && $m{egg_c} >= $eggs[$m{egg}][2]);
		}
		&lv_up;
	}
	# �Ϻސ���
	elsif (!$m{incubation_switch} && $m{egg} && $m{egg_c} >= $eggs[$m{egg}][2]) {
		$m{egg_c} = 0;
		$mes .= "�����Ă���$eggs[$m{egg}][1]���������܂���!<br>";
		
		# ʽ�ڴ��ސ�p����
		if ( $eggs[$m{egg}][1] eq 'ʽ�ڴ���' && rand(7) > 1 && $m{egg} != 53) {
			if (rand(6) > 1) {
				$mes .= "�Ȃ�ƁA$eggs[$m{egg}][1]�̒����� $eggs[$m{egg}][1]���Y�܂�܂���<br>";
			}
			else {
				$mes .= "�Ȃ�ƁA$eggs[$m{egg}][1]�̒��͋���ۂł����c<br>";
				$m{egg} = 0;
			}
		}
		# ���ݴ���
		elsif ($eggs[$m{egg}][1] eq '���ݴ���') {
			$m{egg_c} = 0;
			my @borns = @{ $eggs[$m{egg}][3] };
			my $v = $borns[int(rand(@borns))];
			
			my $pet_mes = $pets[$v][4] ? $pets[$v][4] : '�������[';
			$mes .= "�Ȃ�ƁA$eggs[$m{egg}][1]�̒����� $pets[$v][1] ���Y�܂�܂���<br>$pets[$v][1]��$pet_mes<br><br>$pets[$v][1]�͗a���菊�ɑ����܂���<br>";
			&send_item($m{name}, 3, $v, 0, 0, , int(rand(100))+1);

			# �z�������M���O
			my $ltime = time();
			open my $fh, ">> $logdir/incubation_log.cgi";
			print $fh "$m{name}<>$eggs[$m{egg}][1]<>$pets[$v][1]<>$ltime\n";
			close $fh;
			if (rand(3) < 1) {
				$m{egg} = 0;
			} else {
				$mes .= "$eggs[$m{egg}][1]�������t�s����<br>";
			}
		}
		# ����è���ސ�p����(�j���ɂ��ς��)
		elsif ( $eggs[$m{egg}][1] eq '����è����' ) {
			my($wday) = (localtime($time))[6];
			my @borns = @{ $eggs[5+$wday][3] };
			my $v = $borns[int(rand(@borns))];
			
			my $pet_mes = $pets[$v][4] ? $pets[$v][4] : '�������[';
			$mes .= "�Ȃ�ƁA$eggs[$m{egg}][1]�̒����� $pets[$v][1] ���Y�܂�܂���<br>$pets[$v][1]��$pet_mes<br><br>$pets[$v][1]�͗a���菊�ɑ����܂���<br>";
			&send_item($m{name}, 3, $v, 0, 0, , int(rand(100))+1);

			# �z�������M���O
			my $ltime = time();
			open my $fh, ">> $logdir/incubation_log.cgi";
			print $fh "$m{name}<>$eggs[$m{egg}][1]<>$pets[$v][1]<>$ltime\n";
			close $fh;
			$m{egg} = 0;
		}
		else {
			my @borns = @{ $eggs[$m{egg}][3] };
			my $v = $borns[int(rand(@borns))];
			
			my $pet_mes = $pets[$v][4] ? $pets[$v][4] : '�������[';
			$mes .= "�Ȃ�ƁA$eggs[$m{egg}][1]�̒����� $pets[$v][1] ���Y�܂�܂���<br>$pets[$v][1]��$pet_mes<br><br>$pets[$v][1]�͗a���菊�ɑ����܂���<br>";
			&send_item($m{name}, 3, $v, 0, 0, , int(rand(100))+1);

			# �z�������M���O
			my $ltime = time();
			open my $fh, ">> $logdir/incubation_log.cgi";
			print $fh "$m{name}<>$eggs[$m{egg}][1]<>$pets[$v][1]<>$ltime\n";
			close $fh;
			$m{egg} = 0;
		}

		if ($w{world} eq $#world_states-4) {
			require './lib/fate.cgi';
			&super_attack('incubation');
		}
	}
	# �����ݑ�A���X�̔�����A�����n�̎󂯎��
	elsif (-s "$userdir/$id/money.cgi") {
		if($m{guild_number}){
			open my $fhg1, "< $logdir/guild_shop1_sale.cgi";
			my $lineg1 = <$fhg1>;
			my($g1_sale_c, $g1_sale_money, $g1_update_t) = split /<>/, $lineg1;
			close $fhg1;
			
			open my $fhg2, "< $logdir/guild_shop2_sale.cgi";
			my $lineg2 = <$fhg2>;
			my($g2_sale_c, $g2_sale_money, $g2_update_t) = split /<>/, $lineg2;
			close $fhg2;
			if(($m{guild_number} == 1 && $g1_sale_c > $g2_sale_c) || ($m{guild_number} == 2 && $g2_sale_c > $g1_sale_c)){
				$shop_sale_tax *= $guild_prior_tax_rate;
			}else{
				$shop_sale_tax *= $guild_ferior_tax_rate;
			}
			
			open my $fhg, "< $logdir/bbs_akindo_$m{guild_number}_allmember.cgi";
			my $headline = <$fhg>;
			while (my $line = <$fhg>) {
				my($mname, $vote, $master) = split /<>/, $line;
				if ($master) {
					if($mname eq $m{name}){
						$shop_sale_tax *= $guild_master_tax_rate;
					}
					last;
				}
			}
			close $fhg;
		}
		
		open my $fh, "+< $userdir/$id/money.cgi" or &error("$userdir/$id/money.cgi̧�ق��J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($name, $money, $is_shop_sale) = split /<>/, $line;
			
			if ($money < 0) {
				$m{money} += $money;
				$money *= -1;
				$mes .= "$name�� $money G���x�����܂���<br>";
				
				# ��s�o�c�҂������}�C�i�X�ɂȂ����ꍇ�͋�s�͓|�Y
				if ($m{money} < 0 && -f "$userdir/$id/shop_bank.cgi") {
					unlink "$userdir/$id/shop_bank.cgi";
					unlink "$userdir/$id/shop_sale_bank.cgi";
					&mes_and_send_news("<b>�o�c�����s�͐Ԏ��o�c�̂��ߓ|�Y���܂���</b>", 1);
				}
			}
			elsif ($is_shop_sale eq '1') {
				if ($jobs[$m{job}][1] eq '���l' || $pets[$m{pet}][2] eq 'tax_free') {
					$mes .= "$name���� $money G�̔�������󂯎��܂���<br>";
				}
				else {
					my $v = int($money * $shop_sale_tax);
					$mes .= "$name���� $money G�̔�������󂯎��A$v G�ŋ��Ƃ��Ď���܂���<br>";
					$money -= $v;
				}
				$m{money} += $money;
			}
			elsif ($is_shop_sale eq '2') {
				$mes .= "$name���� $money ���󂯎��܂���<br>";
			}
			else {
				$m{money} += $money;
				$mes .= "$name���� $money G���󂯎��܂���<br>";
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
	}
	elsif (-s "$userdir/$id/ex_c.cgi") {
		open my $fh, "+< $userdir/$id/ex_c.cgi" or &error("$userdir/$id/ex_c.cgi̧�ق��J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($c, $number) = split /<>/, $line;
			&c_up($c) for(1..$number);
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
	}
	elsif (-s "$userdir/$id/cataso_res.cgi") {
		if (!$m{cataso_ratio}) {
			$m{cataso_ratio} = 1500;
		}
		open my $fh, "+< $userdir/$id/cataso_res.cgi" or &error("$userdir/$id/cataso_res.cgi̧�ق��J���܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my($compare, $value) = split /<>/, $line;
			my %c_data = &get_you_datas($compare, 1);
			if (!$c_data{cataso_ratio}) {
				$c_data{cataso_ratio} = 1500;
			}
			my $dr = int(16 + ($c_data{cataso_ratio} - $m{cataso_ratio}) * 0.04 + 0.5);
			if ($dr < 1) {
				$dr = 1;
			} elsif ($dr > 32) {
				$dr = 32;
			}
			$m{cataso_ratio} += int($dr * $value);
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		close $fh;
	}
	elsif ((-s "$userdir/$id/head_hunt.cgi") && $m{random_migrate} ne $w{year}) {
		if ($in{head_hunt} ne '1') {
			open my $fh, "< $userdir/$id/head_hunt.cgi" or &error("$userdir/$id/head_hunt.cgi̧�ق��J���܂���");
			while (my $line = <$fh>) {
				my($hname, $hcountry) = split /<>/, $line;
				$mes .= "$hname���� $cs{name}[$hcountry] �ւ̊��U���󂯂Ă��܂�<br>";
			}
			close $fh;

			$mes .= qq|<form method="$method" action="$script">|;
			$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$mes .= qq|<input type="hidden" name="head_hunt" value="1">|;
			$mes .= qq|<input type="submit" value="���U���󂯂�" class="button1"></form>|;
		}
		else {
			$mes .= "���U���󂯂邱�Ƃɂ��܂���<br>";
			$m{lib} = 'country_move';
			$m{tp} = 100;
			&n_menu;
		}
	}
	# ���ɏ������Ă���ꍇ
	elsif ($m{country}) {
		# Rank UP
		if ($m{rank_exp} >= $m{rank} * $m{rank} * 10 && $m{rank} < $#ranks) {
			$m{rank_exp} -= $m{rank} * $m{rank} * 10;
			++$m{rank};
			my $rank_name = &get_rank_name($m{rank}, $m{name});
			$mes .= "�����̍��ւ̍v�����F�߂��A$m{name}�̊K����$rank_name�ɏ��i���܂���<br>";
		}
		# Rank Down
		elsif ($m{rank_exp} < 0) {
			if ($m{rank} eq '1') {
				$m{rank_exp} = 0;
			}
			else {
				--$m{rank};
				$m{rank_exp} = int($m{rank} * $m{rank} * 10 + $m{rank_exp});
				my $rank_name = &get_rank_name($m{rank}, $m{name});
				$mes .= "$m{name}�̊K����$rank_name�ɍ~�i���܂���<br>";
				if($m{super_rank}){
					$mes .= "������$m{rank_name}�͖��_�E�Ȃ̂Ŗ��̂͂��̂܂܂ł�<br>";
				}
			}
		}
		# ���^
		elsif ($m{country} && $time >= $m{next_salary}) {
			if($m{salary_switch} && $in{get_salary} ne '1'){
				$mes .= qq|<form method="$method" action="$script">|;
				$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
				$mes .= qq|<input type="hidden" name="get_salary" value="1">|;
				$mes .= qq|<input type="submit" value="�������󂯎��" class="button1"></form>|;
			}else{
				$m{egg_c} += int(rand(50)+100) if $m{egg};
				&salary;
			}
		}
	}

	if($m{shogo_t} ne '' || $m{icon_t} ne ''){
		if($time >= $m{trick_time}){
			if($m{shogo_t} ne ''){
				$m{shogo} = $m{shogo_t} unless ($m{shogo} eq $shogos[1][0]);
				$m{shogo_t} = '';
			}
			if($m{icon_t} ne ''){
				if($m{icon} ne $default_icon){
					unlink "$icondir/$m{icon}" or &error("$m{icon}�����݂��܂���");
				}
				$m{icon} = $m{icon_t};
				$m{icon_t} = '';
			}
		}
	}
	if(-s "$userdir/$id/fx.cgi"){
		require './lib/fx_func.cgi';
		$mes .= &check_losscut;
	}

	$y{country} = 0 if $y{country} eq '';
#	$m{act} = 0 if $config_test;
	&run_tutorial_quest('tutorial_full_act_1') if $m{act} > 99;
}

#================================================
# ���^
#================================================
sub salary {
	# ���^��
	sub tax { (100 - $cs{tax}[$m{country}]) * 0.01 };

	$m{next_salary} = int( $time + 3600 * $salary_hour );
	
	my $salary_base = $rank_sols[$m{rank}] * 0.8 + $cs{strong}[$m{country}] * 0.5;
	$salary_base += $cs{strong}[$union] * 0.6 if $union;
	
	my $v = int( $salary_base * &tax ) + 1000;
	
	# �N��Ȃ狋��2.0�{�A���̑�\�҂Ȃ狋��1.5�{
	if ($cs{ceo}[$m{country}] eq $m{name}) {
		$v *= 2.0;
	} elsif (&is_daihyo) {
		$v *= 1.5;
	}
	
	# ���ꍑ�Ȃ��ްŽ
	my($c1, $c2) = split /,/, $w{win_countries};
	if ($c1 eq $m{country}) {
		# �����Ȃ��œ���Ȃ�2�{
		$v *= defined $c2 ? 1.75 : 2;
		$m{egg_c} += int(rand(25)+50) if $m{egg};
	}
	elsif ($c2 eq $m{country}) {
		$v *= 1.75;
		$m{egg_c} += int(rand(25)+50) if $m{egg};
	}
	
	# �ŖS��
	$v *= 0.5 if $cs{is_die}[$m{country}];
	
	# ���l�Ȃ��ްŽ
	$v += 5000 if $jobs[$m{job}][1] eq '���l';
	$v = &use_pet('salary', $v);
	$v = int($v);

	$m{money} += $v;
	$mes .= "$c_m���� $v G�̋��^�����������܂���<br>";
	&write_yran('sal', $v, 1) if $v > 0;
}


#================================================
# ������/���ٱ���
#================================================
sub lv_up {
	$m{exp} -= 100;
	++$m{lv};
	
	# ������
	my $sedai_max = &seed_bonus('sedai_lv', 100);
	if ($m{lv} >= $sedai_max) {
		$m{lv} = 1;
		&c_up('sedai');
		
		# �������Ă����ꍇ
		if ($m{marriage}) {
			&mes_and_world_news("$m{marriage}�Ƃ̊Ԃɂł���$m{sedai}��ڂ̎q���Ɉӎu�������p����܂���", 1);
			
			if ($m{job} eq '25') {
				$m{job} = 15;
			} elsif ($m{job} eq '26') {
				$m{job} = 16;
			} elsif ($m{job} eq '27') {
				$m{job} = 17;
			} elsif ($m{job} eq '28') {
				$m{job} = 18;
			}
			
			for my $k (qw/max_hp max_mp at df mat mdf ag lea cha cha_org/) {
				$m{$k} = int($m{$k} * (rand(0.2)+0.65) );
			}
			$m{rank} -= $m{rank} > 10 ? 2 : 1;
#			$m{rank} -= int(rand(2));
			$m{super_rank} = 0;
			$m{rank_name} = '';
			
			my $y_id = unpack 'H*', $m{marriage};
			if (-f "$userdir/$y_id/user.cgi") {
				my %datas = &get_you_datas($y_id, 1);
				if ($datas{skills}) { # �o���Ă���Z��ۑ�
					open my $fh, "+< $userdir/$id/skill.cgi";
					eval { flock $fh, 2; };
					my $line = <$fh>;
					$line =~ tr/\x0D\x0A//d;
		
					my $is_rewrite = 0;
					for my $skill (split /,/, $datas{skills}) {
						# �o���Ă��Ȃ���قȂ�ǉ�
						unless ($line =~ /,\Q$skill\E,/) {
							$is_rewrite = 1;
							$line .= "$skill,";
						}
					}
					if ($is_rewrite) {
						$line  = join ",", sort { $a <=> $b } split /,/, $line;
						$line .= ',';
						
						seek  $fh, 0, 0;
						truncate $fh, 0;
						print $fh $line;
					}
					close $fh;
				}
				
				if ($pets[$m{pet}][2] eq 'copy_pet' && $datas{pet}) {
					$mes .= "$pets[$m{pet}][1]��$m{pet_c}��$datas{name}���߯Ă�$pets[$datas{pet}][1]���߰���܂���<br>";
					$m{pet} = $datas{pet};
					&get_icon_pet;
				}
				
			}
		}
		# �������Ă��Ȃ��Ƃ�
		else {
			if($m{job} ne '24'){
				&mes_and_world_news("$m{sedai}��ڂւƈӎu�������p����܂���", 1);
			}else{
				&mes_and_world_news("$m{sedai}��ڂւƈӎu�������p����܂������@����$m{name}�̃\\�E���W�F�����^�����ɐ��܂����I", 1);
				open my $bfh, "< $logdir/monster/boss.cgi" or &error("$logdir/monster/boss.cgi̧�ق�����܂���");
				$line = <$bfh>;
				my $boss_name = (split /<>/, $line)[0];
				close $bfh;
				if($boss_name eq '�����C�x���g'){
					$in{boss_at} = $m{at} + 500;
					$in{boss_df} = $m{df} + 500;
					$in{boss_mat} = $m{mat} + 500;
					$in{boss_mdf} = $m{mdf} + 500;
					$in{boss_ag} = $m{ag} + 500;
					$in{boss_cha} = $m{cha} + 500;
					open my $bfh, "> $logdir/monster/boss.cgi" or &error("$logdir/monster/boss.cgi̧�ق�����܂���");
					print $bfh "����$m{name}<>0<>99999<>99999<>$in{boss_at}<>$in{boss_df}<>$in{boss_mat}<>$in{boss_mdf}<>$in{boss_ag}<>$in{boss_cha}<>$m{wea}<>$m{skills}<>$m{mes_lose}<>$m{mes_win}<>$default_icon<>$m{wea_name}<>\n";
					close $bfh;
				}
			}
			
			if ($m{job} eq '25') {
				$m{job} = 15;
			} elsif ($m{job} eq '26') {
				$m{job} = 16;
			} elsif ($m{job} eq '27') {
				$m{job} = 17;
			} elsif ($m{job} eq '28') {
				$m{job} = 18;
			}
			
			if ($pets[$m{pet}][2] eq 'keep_status') {
				$mes .= "$pets[$m{pet}][1]��$m{pet_c}�̗͂ɂ��ð�������̂܂܈����p����܂���<br>";
				$mes .= "��ڂ��I����$pets[$m{pet}][1]��$m{pet_c}�́A���̒��ւƏ����Ă������c<br>";
				&remove_pet;
			}
			else {
				&c_up('boch_c');
				my $down_par = $m{sedai} > 7 ? (rand(0.25)+0.6) : $m{sedai} * 0.05 + 0.35;
				if($m{job} eq '22' || $m{job} eq '23'){
					$down_par = (rand(0.5) + 0.45);
				}
				for my $k (qw/max_hp max_mp at df mat mdf ag lea cha cha_org/) {
					unless($m{job} eq '24' && ($k eq 'max_mp' || $k eq 'cha' || $k eq 'cha_org')){
						$m{$k} = int($m{$k} * $down_par);
					}
				}
				if($m{job} eq '24'){
					$m{job} = 0;
				}
				$m{rank} -= $m{rank} > 10 ? 2 : 1;
				$m{rank} -= int(rand(2));
				$m{super_rank} = 0;
				$m{rank_name} = '';
			}
		}
		if($m{master} && $m{master_c} && $m{sedai} >= 3){
			&graduate;
		}
		# �ȉ����ʂ̏���
		$m{rank} = 1 if $m{rank} < 1;
	
		&use_pet('sedai');
		
		if ($m{skills}) { # �o���Ă���Z��ۑ�
			open my $fh, "+< $userdir/$id/skill.cgi";
			eval { flock $fh, 2; };
			my $line = <$fh>;
			$line =~ tr/\x0D\x0A//d;

			my $is_rewrite = 0;
			for my $skill (split /,/, $m{skills}) {
				# �o���Ă��Ȃ���قȂ�ǉ�
				unless ($line =~ /,\Q$skill\E,/) {
					$is_rewrite = 1;
					$line .= "$skill,";
				}
			}
			if ($is_rewrite) {
				$line  = join ",", sort { $a <=> $b } split /,/, $line;
				$line .= ',';
				
				seek  $fh, 0, 0;
				truncate $fh, 0;
				print $fh $line;
			}
			close $fh;
		}
		if ($pets[$m{pet}][2] eq 'keep_seed') {
			$mes .= "$pets[$m{pet}][1]��$m{pet_c}�̗͂ɂ��푰�����̂܂܈����p����܂���<br>";
			$mes .= "��ڂ��I����$pets[$m{pet}][1]��$m{pet_c}�́A���̒��ւƏ����Ă������c<br>";
			&remove_pet;
			&seed_change('keep');
		} elsif ($pets[$m{pet}][2] eq 'change_seed') {
			$mes .= "$pets[$m{pet}][1]��$m{pet_c}�̗͂ɂ��푰���ς�邩������܂���<br>";
			$mes .= "��ڂ��I����$pets[$m{pet}][1]��$m{pet_c}�́A���̒��ւƏ����Ă������c<br>";
			&remove_pet;
			&seed_change('change');
		} else {
			&seed_change('');
		}
		$m{marriage} = '';
#		&refresh_new_commer;
	}
	# ���x���A�b�v
	else {
		$mes .= "Lv���߁�<br>";
		
		# HP �����͕K���P�ȏ�up����d�l
		my $v = int( rand($jobs[$m{job}][2]) ) + 1;
		$m{max_hp} += $v;
		$mes .= "$e2j{max_hp}+$v ";

		my $count = 3;
		for my $k (qw/max_mp at df mat mdf ag lea cha/) {
			my $v = int( rand($jobs[$m{job}][$count]+1) );
			$m{$k} += $v;
			if ($k eq 'cha') {
				$m{cha_org} += $v;
			}
			$mes .= "$e2j{$k}+$v ";
			++$count;
		}
		
		&use_pet('lv_up');
		&run_tutorial_quest('tutorial_lv_20_1') if $m{lv} == 20;
	}
}

#================================================
# ��q����
#================================================
sub graduate {
	&send_item($m{name}, 2, int(rand($#eggs)+1), 0, 0, 1);
	if(rand(7) > 1){
		&send_item($m{master}, 2, int(rand($#eggs)+1), 0, 0, 1);
	}else{
		require './lib/shopping_offertory_box.cgi';
		&send_god_item(5, $m{master});
	}

	&mes_and_world_news("$m{master}�̒�q�Ƃ��ė��h�ɐ������܂���", 1);
	&regist_you_data($m{master}, 'master', '');
	$m{master} = '';
	$m{master_c} = '';
}

1; # �폜�s��

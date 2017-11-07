require "$datadir/profile.cgi";
#================================================
# ���̨�ِݒ� Created by Merino
#================================================

my @mail_alarm_names = ('���L', '������');
my @mail_alarm_types = ('diary', 'kaizou');

#================================================
sub begin {
	$layout = 2;

	my %datas = ();
	open my $fh, "< $userdir/$id/profile.cgi" or &error("$userdir/$id/profile.cgi̧�ق��J���܂���");
	my $line = <$fh>;
	close $fh;
	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$datas{$k} = $v;
	}

	$mes .= qq|$m{name}�����̨�فF�S�p80����(���p160)�܂�<br>|;
	$mes .= qq|<form method="$method" action="$script"><input type="hidden" name="mode" value="write">|;
	for my $profile (@profiles) {
		if ($profile->[1] eq "�a����") {
			$mes .= qq|<hr>$profile->[1] ���͗�F2000/01/01<br><input type="text" name="$profile->[0]" value="$datas{$profile->[0]}" class="text_box_b"><br>|; 
		}
		else {
			$mes .= qq|<hr>$profile->[1]<br><input type="text" name="$profile->[0]" value="$datas{$profile->[0]}" class="text_box_b"><br>|; 
		}
	}
	if($m{job} eq '22' || $m{job} eq '23' || $m{job} eq '24'){
		my $boch_pet = $m{sex} eq '1' ? '�]����' : 'Ͻ��ķ��';
		$mes .= qq|<hr>$boch_pet<br><input type="text" name="boch_pet" value="$m{boch_pet}" class="text_box_b"><br>|; 
	}
	# ���L�E������ system.cgi ���v�C��
	my @mail_datas = split /,/, $m{mail_address}; # [0]Ұٱ��ڽ [1]���L [2]������
	$mes .= qq|<hr>���[���A�h���X�i�莆�̎�M�ʒm�ɗ��p�j<br><input type="text" name="mail_address" value="$mail_datas[0]" class="text_box_b"><br>|; 

	for my $i (0 .. $#mail_alarm_types) {
		my $checked = $mail_datas[$i+1] ? ' checked' : '';
		$mes .= qq|<input type="checkbox" name="mail_alarm_$mail_alarm_types[$i]" value="1"$checked>$mail_alarm_names[$i] |;
	}
	$mes .= '���l���͕K���ʒm����܂�';

#	if ($w{world} eq $#world_states-4) {
#		require './lib/fate.cgi';
#		$mes .= &regist_mes(0);
#	}
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�ύX����" class="button1"></p></form>|;
	&n_menu;
}

sub tp_1 {
	if ($in{mode} eq 'write') {
		my %datas = ();
		open my $fh, "+< $userdir/$id/profile.cgi" or &error("$userdir/$id/profile.cgi̧�ق��J���܂���");
		eval { flock $fh, 2; };
		my $line = <$fh>;
		for my $hash (split /<>/, $line) {
			my($k, $v) = split /;/, $hash;
			$datas{$k} = $v;
		}
		
		my $is_rewrite = 0;
		for my $profile (@profiles) {
			unless ($in{$profile->[0]} eq $datas{$profile->[0]}) {
				&error("$profile->[1] �ɕs���ȕ���( ,\'\"\;<> )���܂܂�Ă��܂�")	if $in{$profile->[0]} =~ /[;<>]/;
				&error("$profile->[1] �͑S�p80(���p160)�����ȓ��ł�")		if length($in{$profile->[0]}) > 160;
				if ($profile->[0] ne 'birthday') {
					$datas{$profile->[0]} = $in{$profile->[0]};
					$is_rewrite = 1;
				} elsif (!($datas{$profile->[0]} =~ /(\d{4})\/(\d{2})\/(\d{2})/)) {
#					&error("$profile->[1] ���s���ł�(2000/01/01)�̌`���œ��͂��Ă��������B") if &valid_date($in{$profile->[0]});
					$datas{$profile->[0]} = $in{$profile->[0]};
					$is_rewrite = 1;
				}
			}
		}
		if ($is_rewrite) {
			my $new_line = '';
			while ( my($k, $v) = each %datas ) {
				$new_line .= "$k;$v<>";
			}
			
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh $new_line;
			close $fh;
			
			$mes .= '���̨�ق�ύX���܂���<br>';
			&n_menu;
		}
		else {
			close $fh;
			$mes .= '��߂܂���<br>';
		}
		if($m{job} eq '22' || $m{job} eq '23' || $m{job} eq '24'){
			unless ($in{boch_pet} eq $m{boch_pet}){
				&error("�߯Ė��͑S�p10(���p20)�����ȓ��ł�") if length($in{boch_pet}) > 20;
			}
			$m{boch_pet} = $in{boch_pet};
			$mes .= $m{sex} eq '1' ? '�]���łɖ��O��t���܂���<br>':'Ͻ��ķ�ׂɖ��O��t���܂���<br>';
		}

		my @mail_datas = split /,/, $m{mail_address};
		unless ($in{mail_address} eq $mail_datas[0] && $mail_datas[1] eq $in{mail_alarm_diary} && $mail_datas[2] eq $in{mail_alarm_kaizou}) {
			if ($in{mail_address} =~ /^[^@]+@[^.]+\..+/) {
				for my $i (0 .. $#mail_alarm_types) {
					$in{mail_address} .= qq|,$in{"mail_alarm_$mail_alarm_types[$i]"}|;
				}
				$m{mail_address} = $in{mail_address};
				$mes .= '���[���A�h���X��ݒ肵�܂���<br>';
			}
			elsif ($in{mail_address} eq '') {
				$m{mail_address} = '';
				$mes .= '���[���A�h���X���폜���܂���<br>';
			}
			else {
				&error("���͂��ꂽ���[���A�h���X������������܂���");
			}
		}
	}
	else {
		$mes .= '��߂܂���<br>';
	}

	&refresh;
	&n_menu;
}

sub valid_date {
	my $date = shift;
	if ($date =~ /(\d{4})\/(\d{2})\/(\d{2})/) {
		my $year = $1;
		my $month = $2;
		my $day = $3;
		my(@mlast) = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
		
		if ($month < 1 || 12 < $month) { return 1; }
		
		if ($month == 2) {
			if ( (($year % 4 == 0) && ($year % 100 != 0)) || ($year % 400 == 0) ) {
				$mlast[1]++;
			}
		}
		
		if ($day < 1 || $mlast[$month-1] < $day) { return 1; }
		
		return 0;
	}
	return 1;
}

1; # �폜�s��

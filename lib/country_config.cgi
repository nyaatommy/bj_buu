require './lib/move_player.cgi';
my $this_file = "$logdir/violator.cgi";
#=================================================
# ���ݒ� Created by Merino
#=================================================

# �e���ݒ�̓������L���Ȋ���
my $valid_investment = 1;

# �N��̋c���ɂ����ڲ԰�폜����(0:�Ȃ�,1:����)
my $is_ceo_delete = 1;

# �폜��������̏ꍇ�B�K�v�[
my @need_vote_violator = (2, 4, 5);

# �폜��������̏ꍇ�B�K�v�o�ߓ���
my $non_new_commer_date = 30;
my $is_delete = $config_test ? 1 : $m{start_time} + $non_new_commer_date * 24 * 3600 < $time;

my @violate = ('������', '�a��', '�i�v�Ǖ�');

# �폜��������̏ꍇ�B�N��̑��dIP��������(0:�Ȃ�,1:����)
my $is_ceo_watch_multi = 1;

#=================================================
# ���p����
#=================================================
sub is_satisfy {
	if ($m{country} eq '0') {
		$mes .= '���ɑ����ĂȂ��ƍs�����Ƃ��ł��܂���<br>�d������ɂ́u�����v���u�d���v����s���Ă݂�������I��ł�������<br>';
		&refresh;
		&n_menu;
		return 0;
	}
	elsif ($cs{ceo}[$m{country}] ne $m{name}) {
		$mes .= "����$e2j{ceo}�łȂ��ƍs�����Ƃ��ł��܂���<br>";
		&refresh;
		&n_menu;
		return 0;
	}
	return 1;
}

#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '���ɉ����s���܂���?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= "���Y�҂��e����$e2j{ceo}�̓��[�ɂ��폜���邱�Ƃ��ł��܂�<br>" if $is_ceo_delete;
		$mes .= "$c_m�̖��O�A�F�A���j�A��c������S������ύX���邱�Ƃ��ł��܂�<br>";
		$mes .= "$e2j{name}�F$c_m<br>";
		$mes .= "���F�F$cs{color}[$m{country}]<br>";
		$mes .= "��c�����F";
		$mes .= $cs{bbs_name}[$m{country}] eq '' ? "$cs{name}[$m{country}]����c��" : $cs{bbs_name}[$m{country}];
		$mes .= "<br>�S�����F$cs{prison_name}[$m{country}]";
	}
	my @menus = ('��߂�', '����/�F��ύX', '���j/����ق�ύX','NPC����ύX','���ɂ̐ݒ�','�e���ݒ�','��c������ύX','�S������ύX','���y��');
	if ($is_ceo_delete) {
		push @menus, '���Y�ҋc��';
		push @menus, '���Y�Ґ\\��';
		
		if ($is_ceo_watch_multi) {
			push @menus, '���d������';
		}
	}
	&menu(@menus);
}
sub tp_1 {
	return if &is_ng_cmd(1..11);

	$m{tp} = $cmd * 100;
	&{ 'tp_'.$m{tp} };
}

#================================================
# ����/�F��ύX
#================================================
sub tp_100 {
	$mes .= qq|$e2j{name}�͑S�p7(���p14)�����܂ŁB���p�L��(,;"'&)�A��(��߰�)�͎g���܂���<br>|;
	#"
	$mes .= qq|���F��#����n�܂�16�i���\\�L<br>|;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|$e2j{name}�F<input type="text" name="name" value="$c_m" class="text_box1"><br>|;
	$mes .= qq|�F�F<input type="text" name="color" value="$cs{color}[$m{country}]" class="text_box1"><br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�ύX����/��߂�" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_110 {
	my $is_rewrite = 0;
	if ($in{name} || $in{color}) {
		unless ($c_m eq $in{name}) {
			&error("$e2j{name}���L�����Ă�������") if $in{name} eq '';
			&error("$e2j{name}�ɕs���ȕ���( ,;\"\'&<>\\\/ )���܂܂�Ă��܂�") if $in{name} =~ /[,;\"\'&<>\\\/]/;
			#"
			&error("$e2j{name}�ɕs���ȋ󔒂��܂܂�Ă��܂�") if $in{name} =~ /�@/ || $in{name} =~ /\s/;
			&error("$e2j{name}�͑S�p7(���p14)�����܂łł�") if length $in{name} > 14;
			for my $name (@{ $cs{name} }) {
				&error('����$e2j{name}�͂��łɎg���Ă��܂�') if $in{name} eq $name;
			}
			
			$in{color} ||= $cs{color}[$m{country}];
			$mes .= "$e2j{name}��$in{name}�ɕύX���܂���<br>";
			&write_world_news(qq|<b>$c_m��$e2j{ceo}$m{name}�ɂ���āA$c_m��<font color="$in{color}">$in{name}</font>��$e2j{name}�����߂܂���</b>|, 1);
			
			$cs{name}[$m{country}] = $in{name};
			$is_rewrite = 1;
		}
	
		unless ($cs{color}[$m{country}] eq $in{color}) {
			&error('�F�𔼊p�p�����ŋL�����Ă�������') if $in{color} eq '' || $in{color} =~ /[^0-9a-zA-Z#]/;
			&error('�F��#����n�܂�16�i���̐F�ŋL�����Ă�������') if $in{color} !~ /#.{6}/;
			$mes .= "���F��$in{color}�ɕύX���܂���<br>";
			$cs{color}[$m{country}] = $in{color};
			$is_rewrite = 1;
		}
	}

	if ($is_rewrite) {
		&write_cs;
	}
	else {
		$mes .= '��߂܂���<br>';
	}
	
	&begin;
}

#================================================
# ���j��ύX
#================================================
sub tp_200 {
	my $line = &get_countries_mes($m{country});
	my($country_mes, $country_mark, $country_rule) = split /<>/, $line;
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|���j[�S�p100(���p200)�����܂�]<br>�E���s�͍폜����܂�<br>|;
	$mes .= qq|<textarea name="country_mes" cols="60" rows="3" class="textarea1">$country_mes</textarea><br>|;

	$mes .= qq|���[��[�S�p100(���p200)�����܂�]<br>�E���s�͍폜����܂�<br>|;
	$mes .= qq|<textarea name="country_rule" cols="60" rows="3" class="textarea1">$country_rule</textarea><br>|;

	$mes .= qq|<hr>�����<br>|;

	# �����
	$mes .= qq|<input type="radio" name="country_mark" value="">�Ȃ�<hr>|;
	if ($country_mark) {
		my $file_title = &get_goods_title($country_mark);
		$mes .= qq|<input type="radio" name="country_mark" value="$country_mark" checked><img src="$icondir/$country_mark">[���݂̼����]$file_title<hr>|;
	}
	opendir my $dh, "$userdir/$id/picture" or &error("$userdir/$id/picture �ިڸ�؂��J���܂���");
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		next if $file_name =~ /^_/;
		next if $file_name =~ /^index.html$/;
		my $file_title = &get_goods_title($file_name);
		$mes .= qq|<input type="radio" name="country_mark" value="$file_name"><img src="$userdir/$id/picture/$file_name" style="vertical-align:middle;">$file_title<hr>|;
	}
	closedir $dh;

	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�ύX����/��߂�" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_210 {
	unless (defined $in{country_mes}) {
		$mes .= "��߂܂���<br>";
		&begin;
		return;
	}
	
	&error("���̕��j�͑S�p100(���p200)�����܂łł�") if length $in{country_mes} > 200;
	&error("���̕��j�͑S�p100(���p200)�����܂łł�") if length $in{country_rule} > 200;
#	&error("�M�l�c�����V���E�g�V�e�C���m�J�c���J�b�e�C���m�J�c�H") if $w{world} eq $#world_states && $m{country} eq $w{country};
	
	my $is_rewrite = 0;
	my $country = 0;
	my @lines = ();
	open my $fh, "+< $logdir/countries_mes.cgi" or &error("$logdir/countries_mes.cgi̧�ق��J���܂���");
	eval { flock $fh, 2; };
	while (my $line = <$fh>) {
		if ($country eq $m{country}) {
			my($country_mes, $country_mark, $country_rule) = split /<>/, $line;
			
			unless ($country_mes eq $in{country_mes}) {
				$is_rewrite = 1;
				$mes .= "���̕��j��<hr>$in{country_mes}<hr>�ɕύX���܂���<br>";
			}

			unless ($country_rule eq $in{country_rule}) {
				$is_rewrite = 1;
				$mes .= "�Y�@��<hr>$in{country_rule}<hr>�ɕύX���܂���<br>";
			}
			
			# ����ق��聨�Ȃ�
			if ($country_mark && $in{country_mark} eq '') {
				$is_rewrite = 1;
				rename "$icondir/$country_mark", "$userdir/$id/picture/$country_mark" or &error("����ق̏��������Ɏ��s���܂���");
				$mes .= qq|���̼���ق��Ȃ��ɕύX���܂���<br>|;
			}
			# ����ٕύX
			elsif ($country_mark ne $in{country_mark}) {
				&error("�������ق̼���ق����łɎg���Ă��܂�") if -f "$icondir/$in{country_mark}";
				&error("$non_title�̕������قɂ��邱�Ƃ͂ł��܂���") if $in{country_mark} =~ /^_/;
				&error("�I�������G�����݂��܂���") unless -f "$userdir/$id/picture/$in{country_mark}";

				$is_rewrite = 1;
				rename "$icondir/$country_mark", "$userdir/$id/picture/$country_mark" or &error("����ق̏��������Ɏ��s���܂���") if -f "$icondir/$country_mark";
				rename "$userdir/$id/picture/$in{country_mark}", "$icondir/$in{country_mark}" or &error("����ق̏��������Ɏ��s���܂���");
				
				my $file_title = &get_goods_title($in{country_mark});
				$mes .= qq|���̼���ق�$file_title<img src="$icondir/$in{country_mark}">�ɕύX���܂���<br>|;
			}
			
			if ($is_rewrite) {
				$line = "$in{country_mes}<>$in{country_mark}<>$in{country_rule}<>\n";
			}
			else {
				$mes .= "��߂܂���<br>";
				last;
			}
		}
		push @lines, $line;
		++$country;
	}
	if ($country < $m{country}) { # �o�O�ō��̕��j�̐��ƍ��̐�������Ȃ���
		$is_rewrite = 1;
		push @lines, "$in{country_mes}<><><>\n";
	}
	if ($is_rewrite) {
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
	}
	close $fh;

	&begin;
}


#================================================
# NPC���ύX
#================================================
sub tp_300 {
	$mes .= "NPC���ύX";
	$mes .= qq|<form method="$method" action="$script">|;

	require "$datadir/npc_war_$m{country}.cgi";
	for my $i (0..$#npcs) {
		$mes .= qq|<input type="text" name="npc_$i" value="$npcs[$i]{name}" class="text_box1" style="text-align:right"><br>|;
	}
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�ύX����/��߂�" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_310 {
	require "$datadir/npc_war_$m{country}.cgi";
	for my $i (0..$#npcs){
		&error("NPC���ɕs���ȕ���( ,;\"\'&<>\\\/ )���܂܂�Ă��܂�") if $in{"npc_$i"} =~ /[,;\"\'&<>\\\/]/;
		#"
		&error("NPC���ɕs���ȋ󔒂��܂܂�Ă��܂�") if $in{"npc_$i"} =~ /�@/ || $in{"npc_$i"} =~ /\s/;
		&error("NPC���͑S�p7(���p14)�����܂łł�") if length $in{"npc_$i"} > 14;
		unless (defined $in{"npc_$i"}) {
			$mes .= "��߂܂���<br>";
			&begin;
			return;
		}
	}
	
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
	#	[0]����[1]����No	[2]�K�E�Z
		['��', [0],			[61..65],],
		['��', [1 .. 5],	[1 .. 5],],
		['��', [6 ..10],	[11..15],],
		['��', [11..15],	[21..25],],
		['��', [16..20],	[31..35],],
		['��', [21..25],	[41..45],],
		['��', [26..30],	[51..55],],
	);
	
	my $line = qq|\@npcs = (\n|;
	
	for my $i (0..4) {
		$line .= qq|\t{\n\t\tname\t\t=> '$in{"npc_$i"}',\n|;
		
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
	
	open my $fh, "> $datadir/npc_war_$m{country}.cgi";
	print $fh $line;
	close $fh;

	&begin;
}

#================================================
# ���ɐݒ�
#================================================
sub tp_400 {
	$mes .= "���ɐݒ�";
	$mes .= qq|<form method="$method" action="$script">|;
	
	open my $fh, "< $logdir/$m{country}/depot.cgi" or &error("$logdir/$m{country}/depot.cgi ���ǂݍ��߂܂���");
	my $head_line = <$fh>;
	my($lv_s,$sedai_s,$message_s) = split /<>/, $head_line;
	close $fh;
	$mes .= qq|���p�\\���x��<input type="text" name="lv_s" value="$lv_s" class="text_box1" style="text-align:right"><br>|;
	$mes .= qq|���p�\\����<input type="text" name="sedai_s" value="$sedai_s" class="text_box1" style="text-align:right"><br>|;
	$mes .= qq|���b�Z�[�W[�S�p100(���p200)�����܂�]<br>�E���s�͍폜����܂�<br>|;
	$mes .= qq|<textarea name="message_s" cols="60" rows="3" class="textarea1">$message_s</textarea><br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�ύX����/��߂�" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}

sub tp_410 {
	&error("���̕��j�͑S�p100(���p200)�����܂łł�") if length $in{message_s} > 200;
	if (($in{lv_s} > 0 && $in{lv_s} < 99 && $in{lv_s} !~ /[^0-9]/) && ($in{sedai_s} > 0 && $in{sedai_s} < 99 && $in{sedai_s} !~ /[^0-9]/)) {
		my @lines = ();
		open my $fh, "+< $logdir/$m{country}/depot.cgi" or &error("$logdir/$m{country}/depot.cgi���J���܂���");
		eval { flock $fh, 2; };
		my $head_line = <$fh>;
		push @lines, "$in{lv_s}<>$in{sedai_s}<>$in{message_s}<>\n";
		push @lines, $_ while <$fh>;
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
	}
	&begin;
}

#================================================
# �e���ݒ�
#================================================
sub tp_500 {
	if ($time > $w{reset_time}) {
		$mes .= "�e���ݒ�͏I����Ԓ��̂ݍs���܂�<br>";
		&begin;
		return;
	}
	$mes .= "�e���ݒ�";
	$mes .= qq|<form method="$method" action="$script">|;
	my $point = 0;
	unless (-f "$logdir/$m{country}/additional_investment.cgi") {
		open my $fh, "> $logdir/$m{country}/additional_investment.cgi" or &error("$logdir/$m{country}/additional_investment.cgi ���ǂݍ��߂܂���");
		close $fh;
	}
	open my $fh, "< $logdir/$m{country}/additional_investment.cgi" or &error("$logdir/$m{country}/additional_investment.cgi ���ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($since,$name) = split /<>/, $line;
		if ($since + $valid_investment > $w{year}) {
			$point++;
		}
	}
	close $fh;
	$mes .= qq|�U�蕪���\\pt�F$point pt<br>|;
	$mes .= qq|�푈<input type="text" name="war" value="5" class="text_box1" style="text-align:right"><br>|;
	$mes .= qq|����<input type="text" name="dom" value="5" class="text_box1" style="text-align:right"><br>|;
	$mes .= qq|�R��<input type="text" name="mil" value="5" class="text_box1" style="text-align:right"><br>|;
	$mes .= qq|�O��<input type="text" name="pro" value="5" class="text_box1" style="text-align:right"><br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�ύX����/��߂�" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}

sub tp_510 {
	if ($in{war} < 0 || $in{dom} < 0 || $in{mil} < 0 || $in{pro} < 0) {
		$mes .= "0�|�C���g�����ɂ͐ݒ�ł��܂���";
		&begin;
		return;
	}
	my $point = 0;
	open my $fh, "< $logdir/$m{country}/additional_investment.cgi" or &error("$logdir/$m{country}/additional_investment.cgi ���ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($since,$name) = split /<>/, $line;
		if ($since + $valid_investment > $w{year}) {
			$point++;
		}
	}
	close $fh;
	if ($point > 15) {
		$point = 15;
	}
	if ($in{war} + $in{dom} + $in{mil} + $in{pro} != 20) {
		$mes .= "���v20�|�C���g�ɐݒ肵�Ă�������";
		&begin;
		return;
	}
	if (cut_minus($in{war} - 5) + cut_minus($in{dom} - 5) + cut_minus($in{mil} - 5) + cut_minus($in{pro} - 5) > $point) {
		$mes .= "���v$point�|�C���g�ȓ��̕ϓ��ɐݒ肵�Ă�������";
		&begin;
		return;
	}
	
	$cs{modify_war}[$m{country}] = $in{war} - 5;
	$cs{modify_dom}[$m{country}] = $in{dom} - 5;
	$cs{modify_mil}[$m{country}] = $in{mil} - 5;
	$cs{modify_pro}[$m{country}] = $in{pro} - 5;
	
	&write_cs;
	$mes .= "�ݒ肵�܂���<br>";
	
	$mes .= "�푈�F$cs{modify_war}[$m{country}]<br>�����F$cs{modify_dom}[$m{country}]<br>�R���F$cs{modify_mil}[$m{country}]<br>�O���F$cs{modify_pro}[$m{country}]<br>";
	&begin;
}

sub cut_minus {
	$v = shift;
	if ($v < 0) {
		return 0;
	}
	return $v;
}

#================================================
# ��c�����ύX
#================================================
sub tp_600 {
	my $bbs_name = $cs{bbs_name}[$m{country}] eq '' ? "$cs{name}[$m{country}]����c��" : $cs{bbs_name}[$m{country}];

	$mes .= qq|��c�����͑S�p12(���p24)�����܂ŁB���p�L��(,;"'&)�A��(��߰�)�͎g���܂���<br>|;
	#"
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|��c�����F<input type="text" name="bbs_name" value="$bbs_name" class="text_box1"><br>|;
	$mes .= qq|<input type="checkbox" name="default" value="1">��̫�Ăɂ���<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�ύX����/��߂�" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_610 {
	my $is_rewrite = 0;
	if ($in{default} eq '1') {
		$cs{bbs_name}[$m{country}] = ''; # ��̫��

		$mes .= "��c��������̫�ĂɕύX���܂���<br>";

		$is_rewrite = 1;
	}
	elsif ($in{bbs_name}) {
		unless ($cs{bbs_name}[$m{country}] eq $in{bbs_name}) {
			&error("��c�������L�����Ă�������") if $in{bbs_name} eq '';
			&error("��c�����ɕs���ȕ���( ,;\"\'&<>\\\/ )���܂܂�Ă��܂�") if $in{bbs_name} =~ /[,;\"\'&<>\\\/]/;
			#"
			&error("��c�����ɕs���ȋ󔒂��܂܂�Ă��܂�") if $in{bbs_name} =~ /�@/ || $in{bbs_name} =~ /\s/;
			&error("��c�����͑S�p12(���p24)�����܂łł�") if length $in{bbs_name} > 24;

			$mes .= "��c������$in{bbs_name}�ɕύX���܂���<br>";
			
			$cs{bbs_name}[$m{country}] = $in{bbs_name};
			$is_rewrite = 1;
		}
	}

	if ($is_rewrite) {
		&write_cs;
	}
	else {
		$mes .= '��߂܂���<br>';
	}
	
	&begin;
}

#================================================
# �S�����ύX
#================================================
sub tp_700 {
	my $prison_name = $cs{prison_name}[$m{country}] ? $cs{prison_name}[$m{country}] : '�S��';

	$mes .= qq|�S�����͑S�p7(���p14)�����܂ŁB���p�L��(,;"'&)�A��(��߰�)�͎g���܂���<br>|;
	#"
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|��c�����F<input type="text" name="prison_name" value="$prison_name" class="text_box1"><br>|;
	$mes .= qq|<input type="checkbox" name="default" value="1">��̫�Ăɂ���<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�ύX����/��߂�" class="button1"></p></form>|;
	$m{tp} += 10;
	&n_menu;
}
sub tp_710 {
	my $is_rewrite = 0;
	if ($in{default} eq '1') {
		$cs{prison_name}[$m{country}] = '�S��'; # ��̫��

		$mes .= "�S��������̫�ĂɕύX���܂���<br>";

		$is_rewrite = 1;
	}
	elsif ($in{prison_name}) {
		unless ($cs{prison_name}[$m{country}] eq $in{prison_name}) {
			&error("�S�������L�����Ă�������") if $in{prison_name} eq '';
			&error("�S�����ɕs���ȕ���( ,;\"\'&<>\\\/ )���܂܂�Ă��܂�") if $in{prison_name} =~ /[,;\"\'&<>\\\/]/;
			#"
			&error("�S�����ɕs���ȋ󔒂��܂܂�Ă��܂�") if $in{prison_name} =~ /�@/ || $in{prison_name} =~ /\s/;
			&error("�S�����͑S�p7(���p14)�����܂łł�") if length $in{prison_name} > 14;

			$mes .= "�S������$in{prison_name}�ɕύX���܂���<br>";
			
			$cs{prison_name}[$m{country}] = $in{prison_name};
			$is_rewrite = 1;
		}
	}

	if ($is_rewrite) {
		&write_cs;
	}
	else {
		$mes .= '��߂܂���<br>';
	}

	&begin;
}

#================================================
# ���y��
#================================================
sub tp_800 {
	my @lines = &get_country_members($m{country});
	$mes .= '�ȉ��̃v���C���[���L�����N�^�[�폜��]��ł��܂�';
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<table><tr><th></th><th>���O</th></tr>|;
	$mes .= qq|<tr><th><input type="radio" name="suicide" value="" checked/></th><th>������</th></tr>|;
	for my $name (@lines) {
		$name =~ tr/\x0D\x0A//d;
		my %you_datas = &get_you_datas($name);
		if ($pets[$you_datas{pet}][2] eq 'life_down') {
			$mes .= qq|<tr><th><input type="radio" name="suicide" value="$you_datas{name}"/></th><th>$you_datas{name}</th></tr>|;
		}
	}
	$mes .= qq|</table>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="���y��" class="button_s"></form>|;

	$m{tp} += 10;
}
sub tp_810 {
	if ($in{suicide}) {
		my %you_datas = &get_you_datas($in{suicide});
		if ($pets[$you_datas{pet}][2] eq 'life_down') {
			$mes .= "$you_datas{name}��������y�������܂���";
			&move_player($you_datas{name}, $you_datas{country}, 'del');
		}
	}
	&begin;
}

#================================================
# ���Y�ҋc��
#================================================
sub tp_900 {
	unless ($is_ceo_delete && $is_delete) {
		$mes .= "�Q���������ڲ԰�ɂ͌��c��������܂���<br>";
		&begin;
		return;
	}

	$layout = 1;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<input type="submit" value="��߂�" class="button1"></form>|;

	$mes .= "�e��$e2j{ceo}�̋c���ɂ��r�炵�⑽�d�o�^�҂Ȃǂ𗬌Y�����邱�Ƃ��ł��܂�<br>";
	$mes .= "���ȓI�ȍl����NG�B�܂��͊e����\\�]�c��ő��k<br>";
	$mes .= "���F���Y�҂𗬌Y<br>";
	$mes .= "�ی��F�\\������$e2j{ceo}��������Ǖ�<br>";
	$mes .= '<hr>���Y��ؽ�<br>';
	open my $fh, "< $this_file" or &error("$logdir/suspect.cgi̧�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($no, $name, $country, $violator, $message, $yess, $nos, $lv) = split /<>/, $line;
		
		my @yes_c = split /,/, $yess;
		my @no_c  = split /,/, $nos;
		my $yes_c = @yes_c;
		my $no_c  = @no_c;
		
		$lv |= 0;
		
		$mes .= qq|<form method="$method" action="$script"><input type="hidden" name="cmd" value="$no">|;
		$mes .= qq|<font color="$cs{color}[$country]">$cs{name}[$country]</font>��$e2j{ceo}$name���w$violator�x��$violate[$lv]���ׂ��Ǝv���Ă��܂�<br>|;
		$mes .= qq|���R�F$message<br>|;
		$mes .= qq|<input type="radio" name="answer" value="1">�^�� $yes_c�[�F$yess<br>|;
		$mes .= qq|<input type="radio" name="answer" value="2">���� $no_c�[�F$nos<br>|;
		$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$mes .= qq|<input type="submit" value="���[" class="button_s"></form><hr>|;
	}
	close $fh;

	$m{tp} += 10;
}
sub tp_910 {
	unless ($is_ceo_delete && $is_delete) {
		$mes .= "�Q���������ڲ԰�ɂ͌��c��������܂���<br>";
		&begin;
		return;
	}
	if (!$in{answer} || $in{answer} =~ /[^12]/) {
		$mes .= '��߂܂���<br>';
		&begin;
		return;
	}
	
	my @lines = ();
	open my $fh, "+< $this_file" or &error("$this_filȩ�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		my($no, $name, $country, $violator, $message, $yess, $nos, $lv) = split /<>/, $line;
		$lv |= 0;
		
		if ($cmd eq $no) {
			# �\�������̂������Ŕ��΂Ȃ�\�������
			if ($m{name} eq $name && $in{answer} eq '2') {
				$mes .= "$violator��$violate[$lv]�Ґ\\��������܂���<br>";
				next;
			}
			elsif ($m{name} eq $violator) {
				&error("�����̕]�c�ɂ͓��[���邱�Ƃ��ł��܂���");
			}

			my $v_id = unpack 'H*', $violator;
			# �����폜�Ȃǂŏ����Ă����ꍇ�͏��O
			if (!-f "$userdir/$v_id/user.cgi") {
				$mes .= "$violator�Ƃ�����ڲ԰�����݂��܂���<br>";
				next;
			}

			# ���łɎ������ǂ��炩�ɓ���Ă����ꍇ�̂��߂ɁA��񔒎��ɂ���
			my $new_yess = '';
			my $new_nos  = '';
			for my $n (split /,/, $yess) {
				next if $m{country} eq $n;
				$new_yess .= "$n,";
			}
			for my $n (split /,/, $nos) {
				next if $m{country} eq $n;
				$new_nos .= "$n,";
			}
			
			if ($in{answer} eq '1') {
				$new_yess .= "$m{country},";
				$mes .= "$violator��$violate[$lv]�Ɏ^�����܂�<br>";
			}
			elsif ($in{answer} eq '2') {
				$new_nos .= "$m{country},";
				$mes .= "$violator��$violate[$lv]�ɔ��΂��܂�<br>";
			}

			my @yes_c = split /,/, $new_yess;
			my @no_c  = split /,/, $new_nos;
			my $yes_c = @yes_c;
			my $no_c  = @no_c;
			
			if ($yes_c >= $need_vote_violator[$lv]) {
				if($violator eq $admin_name){
					&write_world_news("<b>�y�c���z�e����$e2j{ceo}�B�̕]�c�ɂ��A$cs{name}[$datas{country}]��$violator��$violate[$lv]�ɂȂ�܂����c�Ǝv�������A�o�J��</b>");
					$mes .= "�^����$need_vote_violator�[�ȏ�ɂȂ����̂�$violator��$violate[$lv]�ƂȂ�܂��c�Ǝv�����́H�o�J�Ȃ́H���ʂ́H<br>";
					for my $n (@yes_c) {
						&regist_you_data($cs{ceo}[$n],'shogo','�����t��');
						&regist_you_data($cs{ceo}[$n],'shogo_t','�����t��');
						&regist_you_data($cs{ceo}[$n],'trick_time',$time + 30*24*3600);
					}
				}else{
					if ($lv > 0) {
						my %datas = &get_you_datas($v_id, 1);
						if ($lv > 1) {
							# �ᔽ�҃��X�g�ɒǉ�
							open my $fh2, ">> $logdir/deny_addr.cgi" or &error("$logdir/deny_addr.cgi̧�ق��J���܂���");
							open my $afh, "< $userdir/$v_id/access_log.cgi" or &error("$userdir/$v_id/access_log.cgi̧�ق��J���܂���");
							while ($aline = <$afh>) {
								my ($aaddr, $ahost, $aagent)  = split /<>/, $aline;
								print $fh2 $aagent =~ /DoCoMo/ || $aagent =~ /KDDI|UP\.Browser/
									|| $aagent =~ /J-PHONE|Vodafone|SoftBank/ ? "$aagent\n" : "$aaddr\n";
							}
							close $afh;
							print $fh2 $datas{agent} =~ /DoCoMo/ || $datas{agent} =~ /KDDI|UP\.Browser/
								|| $datas{agent} =~ /J-PHONE|Vodafone|SoftBank/ ? "$datas{agent}\n" : "$datas{addr}\n";
							close $fh2;
						}
						&move_player($violator, $datas{country}, 'trash');
					} else {
						my %datas = &get_you_datas($v_id, 1);
						&move_player($violator, $datas{country}, 0);
						&regist_you_data($datas{name}, 'wt', 7 * 24 * 3600);
						&regist_you_data($datas{name}, 'country', 0);
						&regist_you_data($datas{name}, 'lib', '');
						&regist_you_data($datas{name}, 'tp', 0);
						&regist_you_data($datas{name},'silent_time',$time+7*24*3600);
						&regist_you_data($datas{name},'silent_kind',0);
					}
					&write_world_news("<b>�y�c���z�e����$e2j{ceo}�B�̕]�c�ɂ��A$cs{name}[$datas{country}]��$violator��$violate[$lv]�ɂȂ�܂���<br>���R�F$message</b>");
					$mes .= "�^����$need_vote_violator�[�ȏ�ɂȂ����̂�$violator��$violate[$lv]�ƂȂ�܂�<br>";
				}
			}
			elsif ($no_c > $w{country} - $need_vote_violator[$lv]) {
				my $y_id = unpack 'H*', $name;
				next unless -f "$userdir/$y_id/user.cgi"; # �\�������l�������Ă����ꍇ
				&move_player($name, $country, 0);

				&regist_you_data($name, 'wt', 3 * 24 * 3600);
				&regist_you_data($name, 'country', 0);
				&regist_you_data($name, 'lib', '');
				&regist_you_data($name, 'tp', 0);

				&write_world_news("�y�c���z�e����$e2j{ceo}�B�̕]�c�ɂ��A$cs{name}[$country]��$e2j{ceo}$name�����O�Ǖ��ƂȂ�܂���</b>", 1, $name);
				$mes .= "���΂�$need_vote_violator�[�ȏ�ɂȂ����̂�$name�����O�Ǖ��ƂȂ�܂�<br>";
			}
			else {
				push @lines, "$no<>$name<>$country<>$violator<>$message<>$new_yess<>$new_nos<>$lv<>\n";
			}
		}
		else {
			push @lines, $line;
		}
	}
	seek  $fh, 0, 0;
	truncate $fh, 0;
	print $fh @lines;
	close $fh;
	
	&begin;
}

#================================================
# ���Y�Ґ\��
#================================================
sub tp_1000 {
	unless ($is_ceo_delete && $is_delete) {
		$mes .= "�Q���������ڲ԰�ɂ͐\\����������܂���<br>";
		&begin;
		return;
	}
	$mes .= qq|�������\\�������̂�����ꍇ�́A���Y�ҋc���Ŕ��΂ɓ���Ă�������<br>|;
	$mes .= qq|<hr>���Y�Ґ\\��<br>|;
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|���O�F<input type="text" name="violator" value="$in{violator}" class="text_box1"><br>|;
	$mes .= qq|���R[�S�p40(���p80)�����܂�]�F<br><input type="text" name="message" class="text_box_b">|;
	for my $i (0..$#violate) {
		$mes .= qq|<input type="radio" name="lv" value="$i">$violate[$i]|;
	}
	$mes .= qq|<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="�\\������" class="button1"></p></form>|;
	
	$m{tp} += 10;
	&n_menu;
}
sub tp_1010 {
	unless ($is_ceo_delete && $is_delete) {
		$mes .= "�Q���������ڲ԰�ɂ͐\\����������܂���<br>";
		&begin;
		return;
	}
	if ($in{violator} && $in{message}) {
		&error('���������������܂��S�p40(���p80)�����܂�') if length $in{message} > 80;

		my $y_id = unpack 'H*', $in{violator};
		
		if (-f "$userdir/$y_id/user.cgi") {
			my @lines = ();
			open my $fh, "+< $this_file" or &error("$this_filȩ�ق��J���܂���");
			eval { flock $fh, 2; };
			push @lines, $_ while <$fh>;
			my($last_no) = (split /<>/, $lines[0])[0];
			++$last_no;
			push @lines, "$last_no<>$m{name}<>$m{country}<>$in{violator}<>$in{message}<>$m{country},<><>$in{lv}<>\n";
			seek  $fh, 0, 0;
			truncate $fh, 0;
			print $fh @lines;
			close $fh;
			
			$mes .= "$in{violator}��$in{message}�̗��R��$violate[$in{lv}]�҂Ƃ��Đ\\�����܂���<br>";
		}
		else {
			$mes .= "$in{violator}�Ƃ�����ڲ԰�����݂��܂���<br>";
		}
	}
	else {
		$mes .= '��߂܂���<br>';
	}
	
	&begin;
}

#================================================
# ���d������
#================================================
sub tp_1100 {
	if (!$is_ceo_delete || !$is_ceo_watch_multi) {
		&begin;
		return;
	}

	my @lines = ();
	opendir my $dh, "$userdir" or &error("հ�ް�ިڸ�؂��J���܂���");
	while (my $id = readdir $dh) {
		next if $id =~ /\./;
		next if $id =~ /backup/;
		open my $fh, "< $userdir/$id/user.cgi" or &error("���̂悤����ڲ԰�͑��݂��܂���");
		my $line_data = <$fh>;
		my $line_info = <$fh>;
		close $fh;
		
		my %p = ();
		for my $hash (split /<>/, $line_data) {
			my($k, $v) = split /;/, $hash;
			next if $k =~ /^y_/;
			$p{$k} = $v;
		}
		($p{addr}, $p{host}, $p{agent}) = split /<>/, $line_info;

		my $line = "$id<>";
		for my $k (qw/name shogo country addr host agent ldate/) {
			$line .= "$p{$k}<>";
		}
		push @lines, "$line\n";
	}
	closedir $dh;
	
	@lines = map { $_->[0] }
		sort { $a->[6] cmp $b->[6] || $a->[5] cmp $b->[5] || $a->[7] cmp $b->[7] }
			map { [$_, split /<>/] } @lines;
	
	$layout = 1;
	$mes .= "IP���ڽ�AνĖ��A��׳�ނ������lؽ�<br>";
	$mes .= "�ȉ��̏󋵂ɂ��ؽĂɍڂ邱�Ƃ�����̂ŁA����ؽĂɕ\�����ꂽ�l�����d�Ɗ֘A�t����̂͒���!!<br>";
	$mes .= "���Ǘ������������Ă�����ڲ԰�́A����ڲ԰��۸޲݂��邱�Ƃ��ł���<br>";
	$mes .= "�������n���w�Z�Ȃǂ̌����{�݂���۸޲݂��Ă���ꍇ<br>";
	$mes .= "���g����ڲ԰�̏ꍇ�͂�������������\\��������̂ŗv�m�F!(�g�т̔��ʂ�νĖ��Ŋm�F)<br>";
	$mes .= "�����炳�܂ȑ��d�ȊO�́A�Ƃ肠�����{�l�Ɋm�F���Ă݂邱��<br>";

	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="radio" name="violator" value="" checked>��߂�|;
	$mes .= $is_mobile ? qq|<hr>���O/������/IP���ڽ/νĖ�/��׳��/�X�V��<br>|
		: qq|<table class="table1"><tr><th>���O</th><th>������</th><th>IP���ڽ</th><th>νĖ�</th><th>�X�V��<br></th></tr>|;
	
	my $b_line  = '';
	my $b_addr  = '';
	my $b_host  = '';
	my $b_agent = '';
	my $is_same = 0;
	for my $line (@lines) {
		my($sid, $sname, $sshogo, $scountry, $saddr, $shost, $sagent, $sldate) = split /<>/, $line;
		if ($saddr eq $b_addr && $shost eq $b_host && $sagent eq $b_agent
			|| ($sagent eq $b_agent && ($sagent =~ /DoCoMo/ || $sagent =~ /KDDI|UP\.Browser/ || $sagent =~ /J-PHONE|Vodafone|SoftBank/)) ) {

				unless ($is_same) {
					$is_same = 1;
					my($bid, $bname, $bshogo, $bcountry, $baddr, $bhost, $bagent, $bldate) = split /<>/, $b_line;
					$bname .= "[$bshogo]" if $bshogo;
					$mes .= $is_mobile ? qq|<hr><input type="radio" name="violator" value="$bname">$bname/<font color="$cs{color}[$bcountry]">$cs{name}[$bcountry]/$baddr/$bhost/$bldate<br>|
						: qq|<tr><td><input type="radio" name="violator" value="$bname">$bname</td><td><font color="$cs{color}[$bcountry]">$cs{name}[$bcountry]</font></td><td>$baddr</td><td>$bhost</td><td>$bldate<br></td></tr>|;
				}
					$sname .= "[$sshogo]" if $sshogo;
					$mes .= $is_mobile ? qq|<hr><input type="radio" name="violator" value="$sname">$sname/<font color="$cs{color}[$scountry]">$cs{name}[$scountry]/$saddr/$shost/$sldate<br>|
						: qq|<tr><td><input type="radio" name="violator" value="$sname">$sname</td><td><font color="$cs{color}[$scountry]">$cs{name}[$scountry]</font></td><td>$saddr</td><td>$shost</td><td>$sldate<br></td></tr>|;
		}
		else {
			$b_line  = $line;
			$b_addr  = $saddr;
			$b_host  = $shost;
			$b_agent = $sagent;
			$is_same = 0;
		}
	}
	
	$mes .= qq|</table>| unless $is_mobile;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���Y�Ґ\\��" class="button1"></p></form>|;
	
	$m{tp} += 10;
}
sub tp_1110 {
	if ($in{violator}) {
		$m{tp} = 900;
		&{ 'tp_'.$m{tp} };
	}
	else {
		&begin;
	}
}

1; # �폜�s��

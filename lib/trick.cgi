
#================================================
# ��������
#================================================
#�������炪���ɖ߂鎞��
my $trick_time = 24 * 60 * 60;

#================================================
sub begin {
	$mes .= "�߂�܂�";
	&refresh;
	&n_menu;
}
sub tp_1  {
	$mes .= "�߂�܂�";
	&refresh;
	&n_menu;
}

#================================================
# ��ʸ
#================================================
sub tp_100{
	$mes .= qq|<form method="$method" action="$script"><p>��������ΏہF<input type="text" name="trick_name" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="icon" value="0" checked> ��߂�<hr>|;

	opendir my $dh, "$userdir/$id/picture" or &error('ϲ�߸�����J���܂���');
	while (my $file_name = readdir $dh) {
		next if $file_name =~ /^\./;
		next if $file_name =~ /^_/;
		next if $file_name =~ /\.html$/;

		my $file_title = &get_goods_title($file_name);
		$mes .= qq|<input type="radio" name="icon" value="$file_name"><img src="$userdir/$id/picture/$file_name" $mobile_icon_size> $file_title<hr>|;
	}
	closedir $dh;

	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���̃A�C�R���ɕς���" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_110{
	if ($in{icon} eq '0'){
		$mes .= '��߂܂���<br>';
		&begin;
		return;
	}
	if ($in{trick_name} eq '') {
		$mes .= '��������悪�L������Ă��܂���<br>';
		&begin;
		return;
	}
	if ($in{trick_name} eq $m{name}) {
		$mes .= '�����ɂ�������͂ł��܂���<br>';
		&begin;
		return;
	}
	my $trick_id = unpack 'H*', $in{trick_name};
	my %datas = &get_you_datas($trick_id, 1);
	if ($datas{icon_t} eq ''){
		if ($in{icon} && -f "$userdir/$id/picture/$in{icon}") {
			&error("�������ق̂��̂����łɎg���Ă��܂�") if -f "$icondir/$in{icon}";
			rename "$userdir/$id/picture/$in{icon}", "$icondir/$in{icon}"  or &error("rename error");
			&regist_you_data($in{trick_name},'icon_t',$datas{icon});
			&regist_you_data($in{trick_name},'icon',$in{icon});
			&regist_you_data($in{trick_name},'trick_time',$time + $trick_time);
			&remove_pet;
			&mes_and_world_news("$datas{name}�̱��݂ɂ�����������܂���");
		}
		else {
			$mes .= '��߂܂���<br>';
		}
	}
	&refresh;
	&n_menu;
}

#================================================
# �۽
#================================================
sub tp_200{
	$mes .= qq|<form method="$method" action="$script"><p>��������ΏہF<input type="text" name="trick_name" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="cmd" value="0">��߂�<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>�̍��Ɂi�΁j������<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="��������" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_210{
	return if &is_ng_cmd(1);
	if ($in{trick_name} eq '') {
		$mes .= '��������悪�L������Ă��܂���<br>';
		&begin;
		return;
	}
	if ($in{trick_name} eq $m{name}) {
		$mes .= '�����ɂ�������͂ł��܂���<br>';
		&begin;
		return;
	}
	my $trick_id = unpack 'H*', $in{trick_name};
	my %datas = &get_you_datas($trick_id, 1);
	if ($datas{shogo} && $datas{shogo_t} eq ''){
		my $t_shogo = $datas{shogo};
		$t_shogo .= '(��)';
		&regist_you_data($in{trick_name},'shogo',$t_shogo);
		&regist_you_data($in{trick_name},'shogo_t',$datas{shogo});
		&regist_you_data($in{trick_name},'trick_time',$time + $trick_time);

		&remove_pet;
		&mes_and_world_news("$datas{name}�̏̍���$datas{shogo}����$t_shogo�ɕς��܂���");
	}
	&refresh;
	&n_menu;
}

#================================================
# ���
#================================================
sub tp_300{
	$mes .= qq|<form method="$method" action="$script"><p>��������ΏہF<input type="text" name="trick_name" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="cmd" value="0">��߂�<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>�������𑝌�������<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="��������" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_310{
	return if &is_ng_cmd(1);
	if ($in{trick_name} eq '') {
		$mes .= '��������悪�L������Ă��܂���<br>';
		&begin;
		return;
	}
	if ($in{trick_name} eq $m{name}) {
		$mes .= '�����ɂ�������͂ł��܂���<br>';
		&begin;
		return;
	}
	my $trick_id = unpack 'H*', $in{trick_name};
	my %datas = &get_you_datas($trick_id, 1);
	my $v = int(rand(6)+1) * 10000;
	$mes.="$pets[$m{pet}][1]��$m{pet_c}��$in{trick_name}�̂����� $v G";
	if (rand(2) < 1 && $datas{money} > 10000) {
		$datas{money} -= $v;
		$datas{money} = 10000 if $datas{money} < 10000;
		&regist_you_data($in{trick_name},'money',$datas{money});
		$mes.="���炵�܂���<br>";
	}
	else { 
		$datas{money} += $v;
		&regist_you_data($in{trick_name},'money',$datas{money});
		$mes.="���₵�܂���<br>";
	}

	&remove_pet;
	&mes_and_world_news("$datas{name}�̏������ɂ������炵�܂���");
	&refresh;
	&n_menu;
}

#================================================
# �ٸ���
#================================================
sub tp_400{
	$mes .= qq|<form method="$method" action="$script"><p>�S���ΏہF<input type="text" name="trick_name" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="cmd" value="0">��߂�<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>�����ł��Ȃ�������<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="��������" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_410{
	return if &is_ng_cmd(1);
	if ($in{trick_name} eq '') {
		$mes .= '�S���悪�L������Ă��܂���<br>';
		&begin;
		return;
	}
	if ($in{trick_name} eq $m{name}) {
		$mes .= '�����ɍS���͂ł��܂���<br>';
		&begin;
		return;
	}
	&regist_you_data($in{trick_name},'silent_time', $time + (60 * 20)); # 20��
	&regist_you_data($in{trick_name},'silent_kind', 0);
	&remove_pet if int(rand(3)) < 1;
	&mes_and_world_news("$in{trick_name}�ɉ��D�������܂���");
	&refresh;
	&n_menu;
}

#================================================
# ͯ�����
#================================================
sub tp_500{
	$mes .= qq|<form method="$method" action="$script"><p>���U�ΏہF<input type="text" name="trick_name" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="cmd" value="0">��߂�<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>�����ɗU��<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="���U" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_510{
	return if &is_ng_cmd(1);
	if ($w{world} eq $#world_states || $w{world} eq $#world_states - 5) {
		$mes .= '�����͊��U�ł��܂���<br>';
		&begin;
		return;
	}
	if ($in{trick_name} eq '') {
		$mes .= '���U�悪�L������Ă��܂���<br>';
		&begin;
		return;
	}
	if ($in{trick_name} eq $m{name}) {
		$mes .= '�����Ɋ��U�͂ł��܂���<br>';
		&begin;
		return;
	}

	my $trick_id = unpack 'H*', $in{trick_name};
	my %datas = &get_you_datas($trick_id, 1);
	if ($datas{country} eq $m{country}) {
		$mes .= '�����������U�͂ł��܂���<br>';
		&begin;
		return;
	}
	my $need_money = $datas{sedai} > 100 ? $rank_sols[$datas{rank}]+300000 : $rank_sols[$datas{rank}]+$datas{sedai}*3000;
	if ($m{money} < $need_money) {
		$mes .= '����������܂���<br>';
		&begin;
		return;
	}
	$m{money} -= $need_money;
	$mes .= "����Ƃ���$need_money G�x�����܂���<br>";

	open my $fh, ">> $userdir/$trick_id/head_hunt.cgi";
	print $fh "$m{name}<>$m{country}<>\n";
	close $fh;
	&remove_pet;
	&refresh;
	&n_menu;
}

#================================================
# Ҷ���
#================================================
sub tp_600 {
	$mes .= qq|<form method="$method" action="$script"><p>�������e�F<input type="text" name="topic" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="cmd" value="0">��߂�<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>����<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="����" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_610 {
	return if &is_ng_cmd(1);
	my $is_error = 0;
	if ($in{topic} =~ /[,;\"\'&<>]/) {
		$mes .= "�������e�ɕs���ȕ���( ,;\"\'&<> )���܂܂�Ă��܂�<br>$in{topic}<br>";
		$is_error = 1;
	}
	elsif (length($in{topic}) > 80) {
		$mes .= "�������e�͑S�p40(���p80)�����ȓ��ł�<br>$in{topic}<br>";
		$is_error = 1;
	}
	if ($is_error) {
		&begin;
		return;
	}
	&remove_pet;
	$mes .= "$m{name}��";
	my $place = int(rand(1000));
	if ($place < 950) {
		$mes .= "�L���";
		&_write_news('world_news', "$m{name}�́u$in{topic}�v�Ƌ���");
	}
	elsif ($place < 960) {
		$mes .= "���X�����̏��";
		&write_send_news("$m{name}�́u$in{topic}�v�Ƌ���");
	}
	elsif ($place < 970) {
		$mes .= "���L�u���";
		&write_blog_news("$m{name}�́u$in{topic}�v�Ƌ���");
	}
	elsif ($place < 980) {
		$mes .= "���Z���";
		&write_colosseum_news("$m{name}�́u$in{topic}�v�Ƌ���");
	}
	elsif ($place < 990) {
		$mes .= "�G�̓W�����";
		&write_picture_news("$m{name}�́u$in{topic}�v�Ƌ���");
	}
	elsif ($place < 999) {
		$mes .= "�{����";
		&write_book_news("$m{name}�́u$in{topic}�v�Ƌ���");
	}
	else {
		$mes .= "���E�̒��S��";
		&write_world_big_news("$m{name}�́u$in{topic}�v�Ƌ���");
	}
	$mes .= "�u$in{topic}�v�Ƌ���\n";

	&refresh;
	&n_menu;
}

#================================================
# ��ּ
#================================================
sub tp_700{
	$mes .= qq|<form method="$method" action="$script"><p>��������ΏہF<input type="text" name="trick_name" class="text_box1"></p>|;
	$mes .= qq|<br>�̍��F<input type="text" name="trick_shogo" class="text_box1"><br>|;
	$mes .= qq|<input type="radio" name="cmd" value="0">��߂�<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>�̍�������<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="��������" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_710{
	return if &is_ng_cmd(1);
	if ($in{trick_name} eq '') {
		$mes .= '��������悪�L������Ă��܂���<br>';
		&begin;
		return;
	}
	if ($in{trick_name} eq $m{name}) {
		$mes .= '�����ɂ�������͂ł��܂���<br>';
		&begin;
		return;
	}
	if ($in{trick_shogo} eq '') {
		$mes .= '�̍����L������Ă��܂���<br>';
		&begin;
		return;
	}
	if ($in{trick_shogo} eq $shogos[1][0]) {
		$mes .= '���l���S�~�N�Y�Ă΂��Ƃ������񂾂륥��펯�I�ɍl���ĥ��<br>';
		&begin;
		return;
	}
	$in{trick_shogo} =~ s/��/��/g;
	my $trick_id = unpack 'H*', $in{trick_name};
	my %datas = &get_you_datas($trick_id, 1);
	if ($datas{shogo_t} eq ''){
		&regist_you_data($in{trick_name},'shogo',$in{trick_shogo});
		&regist_you_data($in{trick_name},'shogo_t',$datas{shogo});
		&regist_you_data($in{trick_name},'trick_time',$time + $trick_time);

		&remove_pet;
		&mes_and_world_news("$datas{name}��$in{trick_shogo}�Ƃ����������܂���");
	}
	&refresh;
	&n_menu;
}

#================================================
# �������
#================================================
sub tp_800{
	$mes .= qq|<form method="$method" action="$script"><p>���햼�F<input type="text" name="weapon_name" class="text_box1"></p>|;
	$mes .= qq|<input type="radio" name="cmd" value="0">��߂�<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>�������ɓ����<br>|;
	$mes .= qq|����|;
	$mes .= qq|<input type="radio" name="type" value="0" checked>�I�΂Ȃ�|;
	$mes .= qq|<input type="radio" name="type" value="1" checked>��|;
	$mes .= qq|<input type="radio" name="type" value="2" checked>��|;
	$mes .= qq|<input type="radio" name="type" value="3" checked>��|;
	$mes .= qq|<input type="radio" name="type" value="4" checked>��|;
	$mes .= qq|<input type="radio" name="type" value="5" checked>��|;
	$mes .= qq|<input type="radio" name="type" value="6" checked>��<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="����" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_810{
	return if &is_ng_cmd(1);
	if ($in{weapon_name} eq '') {
		$mes .= '���햼���L������Ă��܂���<br>';
		&begin;
		return;
	}
	if ($m{wea}) {
		# �ؼ��ٕ��펝������Ԃ���������g���Ƶؼ��ٕ���̒��g����߰����Ă��܂�
		# ��߰����邱�Ƃł͂Ȃ����ʰɂȂ��Ė߂��Ă��Ȃ����Ƃ����
		if ($m{wea_name}) {
			&send_item($m{name}, 1, 32, 0, 0, 1); # ���ʰ�
		}
		else {
			&send_item($m{name}, 1, $m{wea}, $m{wea_c}, $m{wea_lv}, 1);
		}
	}
	my $i;
	if ($in{type} >= 1 && $in{type} <= 6) {
		$i = ($in{type} - 1) * 5 + int(rand(5)) + 1
	}
	else {
		$i = int(rand($#weas)+1);
	}

	&remove_pet;
	$m{wea} = $i;

	# �ǂ��������������с�0�ɖ߂�̂Ł�30�ɂȂ邱�Ǝ��̂͂��قǖ��ɂȂ�Ȃ����H
	# �ނ��끚0�����Ă��ԂƁ�30�����Ă��Ԃ�������g�������ɑ������鑤���ł邩��ꗥ��30�ɂ��Ă��܂��Ă��ǂ�����
	# ����ɃI�V���J�f�����b�g
	$m{wea_c} = 0;
	$m{wea_lv} = 30;

	$m{wea_name} = "$in{weapon_name}";
	&mes_and_world_news("$in{weapon_name}����ɓ���܂���");

	&refresh;
	&n_menu;
}

#================================================
# ���
#================================================
sub tp_900 {
	$mes .= qq|<form method="$method" action="$script"><p>�S���ΏہF<input type="text" name="trick_name" class="text_box1"></p><br>|;
	$mes .= qq|<p>��������F<input type="text" name="tail" value="���" class="text_box1"></p><br>|;
	$mes .= qq|<input type="radio" name="cmd" value="0">��߂�<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>���������������<br>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="��������" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_910 {
	return if &is_ng_cmd(1);
	if ($in{trick_name} eq '') {
		$mes .= '�S���悪�L������Ă��܂���<br>';
		&begin;
		return;
	}
	if ($in{tail} eq '') {
		$mes .= '������L������Ă��܂���<br>';
		&begin;
		return;
	}
	if ($in{trick_name} eq $m{name}) {
		$mes .= '�����ɍS���͂ł��܂���<br>';
		&begin;
		return;
	}
	if (length($in{tail}) > 80) {
		$mes .= '����͑S�p40(���p20)�����ȓ��ł�<br>';
		&begin;
		return;
	}
	&regist_you_data($in{trick_name},'silent_time', $time+3600);
	&regist_you_data($in{trick_name},'silent_kind', 4);
	&regist_you_data($in{trick_name},'silent_tail', $in{tail});
	&remove_pet if rand(3) < 1;
	&mes_and_world_news("$in{trick_name}�̌�����������܂���");
	&refresh;
	&n_menu;
}

#================================================
# ΰش
#================================================
sub tp_1000{
	$mes .= qq|<form method="$method" action="$script"><p>�U���v���C���[���F<input type="text" name="trick_name" class="text_box1"></p><br>|;
	$mes .= qq|<p>�U�����F<select name="trick_country" class="menu1">|;
	for my $i (1..$w{country}) {
		$mes .= qq|<option value="$i">$cs{name}[$i]</option>|;
	}
	$mes .= qq|</select></p><br>|;
	$mes .= qq|<p>�߯āF<select name="trick_pet" class="menu1">|;
	for my $i (1..$#pets) {
		$mes .= qq|<option value="$i">$pets[$i][1]</option>|;
	}
	$mes .= qq|</select></p><br>|;
	$mes .= qq|<input type="radio" name="cmd" value="0">��߂�<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="1" checked>�߯Ă𑗂����ӂ������<br>|;
	$mes .= qq|<input type="radio" name="cmd" value="2">�z���U��<br>| if $m{country};
	$mes .= qq|<input type="radio" name="cmd" value="3">���U��<br>| if $m{country};
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="��������" class="button1"></p></form>|;
	$m{tp} += 10;
}
sub tp_1010{
	if ($in{trick_name} eq '') {
		$mes .= '�������疼���L������Ă��܂���<br>';
		&begin;
		return;
	}
	if ($cmd eq '1') {
		&mes_and_send_news("$in{trick_name}��$pets[$in{trick_pet}][1]�𑗂�܂���");
	}
	elsif ($cmd eq '2') {
		&write_world_news("<b>$cs{name}[$m{country}]��$in{trick_name}��</b><b>$cs{name}[$in{trick_country}]�ɐ��z�������܂���</b>");
	}
	elsif ($cmd eq '3') {
		&write_world_news("<b>$cs{name}[$m{country}]��$in{trick_name}��</b><b>$cs{name}[$in{trick_country}]�ƒ��������т܂���</b>");
	}
	else {
		$mes .= '��߂܂���<br>';
		&begin;
		return;
	}
	&remove_pet if rand(7) < 1;
	&refresh;
	&add_prisoner;
	&n_menu;
}

1; # �폜�s��

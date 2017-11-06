#!/usr/local/bin/perl --
require 'config.cgi';
require 'config_game.cgi';
require "$datadir/skill.cgi";
require "$datadir/profile.cgi";
#================================================
# �ð�� & ���̨�ٕ\�� Created by Merino
#================================================

&decode;
&header;
&header_profile;
&read_cs;

#my table1 = $is_smart ? "table2" : "table1" ;

if    ($in{mode} eq 'profile') { &profile; }
elsif ($is_mobile) { &status_mobile if $in{mode} eq 'status'; }
else { &status_pc; }

&footer;
exit;

#================================================
# �g�ѽð�����
#================================================
sub status_mobile {
	%m = &get_you_datas($in{id}, 1);
	my %m_year = &get_you_year_data($in{id});

	my %collection_pars = &collection_pars;
	my $skill_par = &skill_par;
	my $shogo_par = &shogo_par;
	my $war_c   = $m{win_c} + $m{lose_c} + $m{draw_c};
	my $win_par = $m{win_c} <= 0 ? 0 : int($m{win_c} / $war_c * 1000) * 0.1;
	
	my $skill_info = '';
	for my $m_skill (split /,/, $m{skills}) {
		$skill_info .= "[$skills[$m_skill][2]]$skills[$m_skill][1]<br>";
	}

	my ($day, $mon, $year) = (localtime($m{start_time}))[3..5];
	my ($day2, $mon2, $year2) = (localtime($time))[3..5];
	my $start_day = sprintf('%04d/%02d/%02d', $year + 1900, $mon + 1, $day);
	my $time1 = timelocal(0, 0, 0, $day, $mon, $year);
	my $time2 = timelocal(0, 0, 0, $day2, $mon2, $year2);
	my $gaming_day = int(($time2 - $time1) / (60*60*24));

	print qq|�X�V���� $m{ldate}<br>|;
	print qq|�Q���� $start_day($gaming_day��)<hr>|;

	print qq|<img src="$icondir/$m{icon}" style="vertical-align: middle;" $mobile_icon_size>| if $m{icon};
	print qq|<img src="$icondir/pet/$m{icon_pet}" style="vertical-align: middle;" $mobile_icon_size>>| if $m{icon_pet};
	print qq|$m{name}<br>|;
	if ($m{marriage}) {
		my $yid = unpack 'H*', $m{marriage};
		print qq|�������� <a href="profile.cgi?id=$yid">$m{marriage}</a><br>|;
	}
	if ($m{master}) {
		my $yid = unpack 'H*', $m{master};
		if($m{master_c}){
			print qq|�t�� <a href="profile.cgi?id=$yid">$m{master}</a><br>|;
		}else{
			print qq|��q <a href="profile.cgi?id=$yid">$m{master}</a><br>|;
		}
	}
	my $rank_name = &get_rank_name($m{rank}, $m{name});
	if ($m{super_rank}){
		$rank_name = '';
		$rank_name .= '��' for 1 .. $m{super_rank};
		$rank_name .= $m{rank_name};
	}
	print qq|<font color="$cs{color}[$m{country}]">$cs{name}[$m{country}]</font> $rank_name<br>|;
	print qq|$units[$m{unit}][1]<br>|;
	print qq|�̍� $m{shogo}<br>| if $m{shogo};
	print qq|Lv.<b>$m{lv}</b>|;
	print qq|���� <b>$m{money}</b> G<br>|;
	my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
	my $pet_c = $m{pet} > 0 ? "��$m{pet_c}": ($m{pet} < 0 ? "($m{pet_c}/$pets[$m{pet}][5])" : '');
	my $petname = "$pets[$m{pet}][1]$pet_c";
	if($m{job} eq '22' || $m{job} eq '23' || $m{job} eq '24'){
		if($m{boch_pet}){
			$petname = $m{boch_pet};
		}
	}
	print qq|<font color="#9999CC">����:[$weas[$m{wea}][2]]$wname��<b>$m{wea_lv}</b></font><br>| if $m{wea};
	print qq|<font color="#9999CC">�h��:[$guas[$m{gua}][2]]$guas[$m{gua}][1]</font><br>| if $m{gua};
	print qq|<font color="#99CCCC">�߯�:$petname</font><br>| if $m{pet};
	print qq|<font color="#99CC99">�Ϻ�:$eggs[$m{egg}][1]</font><br>| if $m{egg};

	my $m_st = &m_st;
	print <<"EOM";
		<b>$m{sedai}</b>�����<br>
		$sexes[ $m{sex} ] [$jobs[$m{job}][1]][$seeds{$m{seed}}[0]]<br>
		�M�� <b>$m{medal}</b>��<br>
		���ɺ�� <b>$m{coin}</b>��<br>
		<hr>
		�y�ð���z����:$m_st<br>
		$e2j{max_hp} [<b>$m{max_hp}</b>]/�l�o [<b>$m{max_mp}</b>]/<br>
		$e2j{at} [<b>$m{at}</b>]/$e2j{df} [<b>$m{df}</b>]/<br>
		$e2j{mat} [<b>$m{mat}</b>]/$e2j{mdf} [<b>$m{mdf}</b>]/<br>
		$e2j{ag} [<b>$m{ag}</b>]/$e2j{cha} [<b>$m{cha}</b>]/<br>
		$e2j{lea} [<b>$m{lea}</b>]<br>
		<hr>
		�y�o���Ă���Z�z<br>
		 $skill_info
		<hr>
		�y�n���x�z<br>
		�_�� <b>$m{nou_c}</b>/���� <b>$m{sho_c}</b>/���� <b>$m{hei_c}</b>/�O�� <b>$m{gai_c}</b>/�ҕ� <b>$m{mat_c}</b>/<br>
		���D <b>$m{gou_c}</b>/���� <b>$m{cho_c}</b>/���] <b>$m{sen_c}</b>/�E�� <b>$m{esc_c}</b>/�~�o <b>$m{res_c}</b>/<br>
		��@ <b>$m{tei_c}</b>/�U�v <b>$m{gik_c}</b>/�U�� <b>$m{kou_c}</b>/���� <b>$m{cas_c}</b>/���� <b>$m{mon_c}</b>/<br>
		�C�s <b>$m{shu_c}</b>/���� <b>$m{tou_c}</b>/���Z <b>$m{col_c}</b>/ڰ�  <b>$m{cataso_ratio}</b>/no1 <b>$m{no1_c}</b>/<br>
		���� <b>$m{hero_c}</b>/���� <b>$m{huk_c}</b>/�ŖS <b>$m{met_c}</b>/�� <b>$m{fes_c}</b>/<br>
		<hr>
		�y��\\���߲�āz<br>
		�푈 <b>$m{war_c}</b>/���� <b>$m{dom_c}</b>/�R�� <b>$m{mil_c}</b>/�O�� <b>$m{pro_c}</b>/
		<hr>
		�y����z<br>
		<b>$war_c</b>�� <b>$m{win_c}</b>�� <b>$m{lose_c}</b>�� <b>$m{draw_c}</b>��<br>
		���� <b>$win_par</b>%
		<hr>
		�y����ذė��z<br>
		�̍�<b>$shogo_par</b>%<br>
		���<b>$skill_par</b>%<br>
		����<b>$collection_pars{1}</b>%<br>
		�h��<b>$collection_pars{4}</b>%<br>
		�Ϻ�<b>$collection_pars{2}</b>%<br>
		�߯�<b>$collection_pars{3}</b>%<br>
		<hr>
		�y��N�x���сz<br>
		�D���� <b>$m_year{strong}</b>/�_�� <b>$m_year{nou}</b>/���� <b>$m_year{sho}</b>/���� <b>$m_year{hei}</b>/<br>
EOM
}

#================================================
# PC�ð�����
#================================================
sub status_pc {
	%m = &get_you_datas($in{id}, 1);
	my %m_year = &get_you_year_data($in{id});

	my %collection_pars = &collection_pars;
	my $skill_par = &skill_par;
	my $shogo_par = &shogo_par;
	my $war_c   = $m{win_c} + $m{lose_c} + $m{draw_c};
	my $win_par = $m{win_c} <= 0 ? 0 : int($m{win_c} / $war_c * 1000) * 0.1;
	
	my $skill_info = '';
	for my $m_skill (split /,/, $m{skills}) {
		$skill_info .= qq|<tr><td align="center">$skills[$m_skill][2]</td><td>$skills[$m_skill][1]</td></tr>|;
	}
	
	my $rank_name = &get_rank_name($m{rank}, $m{name});
	$m{name} .= "[$m{shogo}]" if $m{shogo};
	if ($m{super_rank}){
		$rank_name = '';
		$rank_name .= '��' for 1 .. $m{super_rank};
		$rank_name .= $m{rank_name};
	}
	
#	print qq|<table width="440" border="0" cellpadding="3" bgcolor="#CCCCCC"><tr><td bgcolor="#000000" align="left" valign="top">|;
	print qq|<table border="0" cellpadding="3" bgcolor="#CCCCCC"><tr><td bgcolor="#000000" align="left" valign="top">|;
	print qq|<table width="100%" border="0"><tr><td width="60%" valign="top" align="left"><tt>|;
	print qq|<img src="$icondir/$m{icon}" style="vertical-align: middle;">| if $m{icon};
	print qq|$m{name}<br>|;
	if ($m{marriage}) {
		my $yid = unpack 'H*', $m{marriage};
		print qq|�������� <a href="profile.cgi?id=$yid">$m{marriage}</a><br>|;
	}
	if ($m{master}) {
		my $yid = unpack 'H*', $m{master};
		if($m{master_c}){
			print qq|�t�� <a href="profile.cgi?id=$yid">$m{master}</a><br>|;
		}else{
			print qq|��q <a href="profile.cgi?id=$yid">$m{master}</a><br>|;
		}
	}

	my $m_st = &m_st;
	my $wname = $m{wea_name} ? $m{wea_name} : $weas[$m{wea}][1];
	my $pet_c = $m{pet} > 0 ? "��$m{pet_c}": ($m{pet} < 0 ? "($m{pet_c}/$pets[$m{pet}][5])" : '');
	my $petname = "$pets[$m{pet}][1]$pet_c";
	if($m{job} eq '22' || $m{job} eq '23' || $m{job} eq '24'){
		if($m{boch_pet} && $m{pet}){
			$petname = $m{boch_pet};
		}
	}
	my $pet_icon = qq|<p><img src="$icondir/pet/$m{icon_pet}" style="vertical-align: middle;"></p>| if $m{icon_pet};
	my ($day, $mon, $year) = (localtime($m{start_time}))[3..5];
	my ($day2, $mon2, $year2) = (localtime($time))[3..5];
	my $start_day = sprintf('%04d/%02d/%02d', $year + 1900, $mon + 1, $day);
	my $time1 = timelocal(0, 0, 0, $day, $mon, $year);
	my $time2 = timelocal(0, 0, 0, $day2, $mon2, $year2);
	my $gaming_day = int(($time2 - $time1) / (60*60*24));
	print <<"EOM";
		<font color="$cs{color}[$m{country}]">$cs{name}[$m{country}]</font> $rank_name<br>
		$units[$m{unit}][1]
		<hr size="1" width="90%">
			<font color="#9999CC">����F[$weas[$m{wea}][2]]$wname��<b>$m{wea_lv}</b></font><br>
			<font color="#9999CC">�h��F[$guas[$m{gua}][2]]$guas[$m{gua}][1]</font><br>
			<font color="#99CCCC">�߯āF$petname</font><br>
			<font color="#99CC99">�ϺށF$eggs[$m{egg}][1]</font><br>
		</tt></td><td valign="top" align="left"><tt>
			<b>$m{sedai}</b>����� $sexes[ $m{sex} ]<br>
			Lv.<b>$m{lv}</b> [$jobs[$m{job}][1]][$seeds{$m{seed}}[0]]<br>
			<hr size="1">
			���� <b>$m{money}</b>G<br>
			<hr size="1">
			�M�@�́@<b>$m{medal}</b>��<br>
			���ɺ�� <b>$m{coin}</b>��<br>
			<p>�X�V���� $m{ldate}<br>$start_day $gaming_day��</p>
			$pet_icon
		</tt></td></tr></table>
		<tt>

		�y�ð���z�����F$m_st<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>$e2j{max_hp}</th><td align="right">$m{max_hp}</td>
			<th>$e2j{at}</th><td align="right">$m{at}</td>
			<th>$e2j{df}</th><td align="right">$m{df}</td>
		</tr><tr>
			<th>�l�o</th><td align="right">$m{max_mp}</td>
			<th>$e2j{mat}</th><td align="right">$m{mat}</td>
			<th>$e2j{mdf}</th><td align="right">$m{mdf}</td>
		</tr><tr>
			<th>$e2j{lea}</th><td align="right">$m{lea}</td>
			<th>$e2j{ag}</th><td align="right">$m{ag}</td>
			<th>$e2j{cha}</th><td align="right">$m{cha}</td>
		</tr>
		</table>
		<hr size="1">
		�y�o���Ă���Z�z<br>
		<table class="table1" cellpadding="3">
		<tr><th>����</th><th>�Z�@��</th></tr>
		$skill_info
		</table>

		<hr size="1">
		�y�n���x�z<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>�_��</th><td align="right">$m{nou_c}</td>
			<th>����</th><td align="right">$m{sho_c}</td>
			<th>����</th><td align="right">$m{hei_c}</td>
			<th>�O��</th><td align="right">$m{gai_c}</td>
			<th>�ҕ�</th><td align="right">$m{mat_c}</td>
		</tr>
		<tr>
			<th>���D</th><td align="right">$m{gou_c}</td>
			<th>����</th><td align="right">$m{cho_c}</td>
			<th>���]</th><td align="right">$m{sen_c}</td>
			<th>�E��</th><td align="right">$m{esc_c}</td>
			<th>�~�o</th><td align="right">$m{res_c}</td>
		</tr>
		<tr>
			<th>��@</th><td align="right">$m{tei_c}</td>
			<th>�U�v</th><td align="right">$m{gik_c}</td>
			<th>�U��</th><td align="right">$m{kou_c}</td>
			<th>����</th><td align="right">$m{cas_c}</td>
			<th>����</th><td align="right">$m{mon_c}</td>
		</tr>
		<tr>
			<th>�C�s</th><td align="right">$m{shu_c}</td>
			<th>����</th><td align="right">$m{tou_c}</td>
			<th>���Z</th><td align="right">$m{col_c}</td>
			<th>ڰ�</th><td align="right">$m{cataso_ratio}</td>
			<th>no1</th><td align="right">$m{no1_c}</td>
		</tr>
		<tr>
			<th>����</th><td align="right">$m{hero_c}</td>
			<th>����</th><td align="right">$m{huk_c}</td>
			<th>�ŖS</th><td align="right">$m{met_c}</td>
			<th>��</th><td align="right">$m{fes_c}</td>
			<th>�@</th><td align="right">�@</td>
		</tr>
		</table>
		
		<hr size="1">
		�y��\\���߲�āz<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>�푈</th><td align="right">$m{war_c}</td>
			<th>����</th><td align="right">$m{dom_c}</td>
			<th>�R��</th><td align="right">$m{mil_c}</td>
			<th>�O��</th><td align="right">$m{pro_c}</td>
		</tr>
		</table>
		
		<hr size="1">
		�y����z<br>
		<table class="table1" cellpadding="3">
		<tr>
			<th>���</th><td align="right">$war_c</td>    
			<th>����</th><td align="right">$m{win_c}</td> 
			<th>����</th><td align="right">$m{lose_c}</td>
			<th>����</th><td align="right">$m{draw_c}</td>
			<th>����</th><td align="right">$win_par %</td>
		</tr>
		</table>
		
		<hr size="1">
		�y����ذė��z<br>
		<table class="table1" cellpadding="3">
			<tr>
				<th>�̍�</th><td align="right"><b>$shogo_par</b>%<br></td>
				<th>���</th><td align="right"><b>$skill_par</b>%<br></td>
				<th>�Ϻ�</th><td align="right"><b>$collection_pars{2}</b>%<br></td>
			</tr>
			<tr>
				<th>����</th><td align="right"><b>$collection_pars{1}</b>%<br></td>
				<th>�h��</th><td align="right"><b>$collection_pars{4}</b>%<br></td>
				<th>�߯�</th><td align="right"><b>$collection_pars{3}</b>%<br></td>
			</tr>
		</table>
		
		<hr size="1">
		�y��N�x���сz<br>
		<table class="table1" cellpadding="3">
			<tr>
				<th>�D����</th><td align="right"><b>$m_year{strong}</b></td>
				<th>�_��</th><td align="right"><b>$m_year{nou}</b></td>
				<th>����</th><td align="right"><b>$m_year{sho}</b></td>
				<th>����</th><td align="right"><b>$m_year{hei}</b><br></td>
			</tr>
		</table>
	</tt></td></tr></table>
EOM
}

#================================================
# ���̨��
#================================================
sub profile {
	open my $fh, "< $userdir/$in{id}/profile.cgi" or &error("$userdir/$in{id}/profile.cgi ̧�ق��ǂݍ��߂܂���");
	my $line = <$fh>;
	close $fh;
	my %datas = ();
	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		$datas{$k} = $v;
	}
	
#	print qq|<table class="table1" cellpadding="3" width="440">| unless $is_mobile;
	print qq|<table class="table1" cellpadding="3">| unless $is_mobile;
	for my $profile (@profiles) {
		next if $datas{$profile->[0]} eq '';
		
		# ����ݸ(BBS��CHAT�ƈႢ�ҏW�\�Ȃ̂ŁA�ҏW����Ƃ����ݸ��ނ��o�Ă��܂��̂œǂݍ��݂ŵ���ݸ����)
		$datas{$profile->[0]} =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\=\@\;\#\:\%]+)/$1<a href=\"$2\" target=\"_blank\">$2<\/a>/g;
		$is_mobile ? $datas{$profile->[0]} =~ s|�n�@�g|<font color="#FFB6C1">&#63726;</font>|g : $datas{$profile->[0]} =~ s|�n�@�g|<font color="#FFB6C1">&hearts;</font>|g;
		
		print $is_mobile ? qq|<hr><h2>$profile->[1]</h2><br>$datas{$profile->[0]}<br>|
			: qq|<tr><th align="left">$profile->[1]</th></tr><tr><td>$datas{$profile->[0]}</td></tr>|;
	}
	print qq|</table>| unless $is_mobile;
}


#================================================
# �e����ذė�
#================================================
sub skill_par { # �Z
	open my $fh, "< $userdir/$in{id}/skill.cgi" or &error("$userdir/$in{id}/skill.cgi̧�ق��ǂݍ��߂܂���");
	my $line = <$fh>;
	close $fh;
	$line =~ tr/\x0D\x0A//d;
	
	my @nos = split /,/, $line;
	pop @nos; # �擪�̋������
	
	my $comp_par = @nos <= 0 ? 0 : int(@nos / $#skills * 100);
	$comp_par = 100 if $comp_par > 100;
	return $comp_par;
}
sub shogo_par { # �̍�
	my $count = 0;
	for my $i (1 .. $#shogos) {
		my($k, $v) = each %{ $shogos[$i][1] };
		++$count if $m{$k} >= $v;
	}
	my $comp_par = $count <= 0 ? 0 : int($count / ($#shogos-2) * 100);
	$comp_par = 100 if $comp_par > 100;
	return $comp_par;
}

sub collection_pars { # ����
	my %pars = ();
	my $kind = 1;
	open my $fh, "< $userdir/$in{id}/collection.cgi" or &error("$userdir/$in{id}/collection.cgi̧�ق��ǂݍ��߂܂���");
	while (my $line = <$fh>) {
		$line =~ tr/\x0D\x0A//d;
		my @nos = split /,/, $line;
		pop @nos; # �擪�̋������
		
		if (@nos <= 0) {
			$pars{$kind} = 0;
		}
		elsif ($kind eq '1') {
			$pars{$kind} = int(@nos / $#weas * 100);
		}
		elsif ($kind eq '2') {
			$pars{$kind} = int(@nos / ($#eggs - 1) * 100);
		}
		elsif ($kind eq '3') {
			$pars{$kind} = int(@nos / ($#pets - 5) * 100);
		}
		elsif ($kind eq '4') {
			$pars{$kind} = int(@nos / ($#guas - 4) * 100);
		}
		$pars{$kind} = 100 if $pars{$kind} > 100;
		++$kind;
	}
	close $fh;
	
	return %pars;
}

#================================================
# ��N�����L���O�f�[�^�擾
#================================================
sub get_you_year_data {
	my $player_id = shift;
	
	my $last_year = $w{year} - 1;
	
	if (-f "$userdir/$player_id/year_ranking.cgi") {
		open my $fh, "< $userdir/$player_id/year_ranking.cgi" or &error("year_ranking.cgi̧�ق��J���܂���");
		while (my $line = <$fh>) {
			my %ydata;
			for my $hash (split /<>/, $line) {
				my($k, $v) = split /;/, $hash;
				$ydata{$k} = $v;
				if($k eq 'year'){
					if($v != $last_year){
						next;
					}
				}
			}
			if($ydata{year} == $last_year){
				return %ydata;
			}
		}
		close $fh;
	}
	return ();
}


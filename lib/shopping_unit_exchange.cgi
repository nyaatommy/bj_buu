$mes .= qq|勲章 $m{medal}個<br>| if $is_mobile;
#=================================================
# 部隊変更 Created by Merino
#=================================================

# 勲章1個の金額
my $exchange_money = 3000;

# ★30武器の価値
my $exchange_medal = $m{wea} == 0 ? 0:
					$m{wea} <= 30 ? (($m{wea} - 1) % 5 + 1) * 5:
					($m{wea} % 5 + 5) * 5;

# 引き換え品
my @prizes = (
# 種類 1=武器,2=卵,3=ﾍﾟｯﾄ 
#	[0]種類,[1]No,[2]勲章
	[0,	0,	0,	],
	[2,	24,	2,	], # ﾌﾞﾗｯﾄﾞｴｯｸﾞ
	[2,	51,	3,	], # ﾋﾞｷﾞﾅｰｴｯｸﾞ
	[1,	12,	5,	], # ﾄﾏﾎｰｸ
	[1,	17,	5,	], # ｴﾙﾌｧｲｱｰ
	[1,	27,	5,	], # ｴﾙｻﾝﾀﾞｰ
	[3,	126,	15,	], # ｽﾘｰﾌﾟｼｰﾌﾟ
	[2,	21,	15,	], # ﾚｼﾞｪﾝﾄﾞｴｯｸﾞ
	[3,	184,	18,	], # ﾚﾝｼﾞ
	[2,	33,	20,	], # ｳｪﾎﾟﾝｴｯｸﾞ
	[2,	27,	25,	], # ﾊﾟﾝﾄﾞﾗｴｯｸﾞ
	[2,	3,	30,	], # ﾄﾞﾘｰﾑｴｯｸﾞ
	[2,	45,	80,	], # ｴﾝﾄﾞｴｯｸﾞ
	[2,	37,	90,	], # ｺﾞｯﾄﾞｴｯｸﾞ
	[2,	46,	99,	], # ﾊﾞﾂｴｯｸﾞ
);

# 特別条件でｸﾗｽﾁｪﾝｼﾞできるもの
my %plus_needs = (
# 部隊No => 条件文,					if条件									# 条件ｸﾘｱ後の処理
	7  => ['ﾀﾞｰｸﾎｰｽを生贄',			sub{ $pets[$m{pet}][2] eq 'speed_up' },	sub{ $mes.="$pets[$m{pet}][1]★$m{pet_c}を生贄にしました<br>"; &remove_pet; } ],
	8  => ['ﾄﾞﾗｺﾞﾝ系のﾍﾟｯﾄを生贄',	sub{ $pets[$m{pet}][1] =~ /ﾄﾞﾗｺﾞﾝ/ },	sub{ $mes.="$pets[$m{pet}][1]★$m{pet_c}を生贄にしました<br>"; &remove_pet; } ],
	11 => ['職業が忍者',			sub{ $jobs[$m{job}][1] eq '忍者' },		sub{} ],
	12 => ["$eggs[23][1]を生贄",	sub{ $m{egg} eq '23'},					sub{ $mes.="$eggs[$m{egg}][1]を生贄にしました<br>"; $m{egg} = 0; $m{egg_c} = 0; } ],
	15 => ['職業が魔物使い',		sub{ $jobs[$m{job}][1] eq '魔物使い' },	sub{} ],
	16 => ['ｸﾛﾉｽを生贄+内政熟練度が計5000以上',			sub{ ($pets[$m{pet}][0] eq '42' && $m{nou_c}+$m{sho_c}+$m{hei_c}>=5000) },	sub{$mes.="$pets[$m{pet}][1]★$m{pet_c}を生贄にしました<br>"; &remove_pet;} ],
	17 => ['ｺﾞｰｽﾄを生贄+奪軍事3種熟練度が計10000以上',			sub{ ($pets[$m{pet}][2] eq 'no_ambush' && $m{gou_c}+$m{cho_c}+$m{sen_c}>=10000) },	sub{$mes.="$pets[$m{pet}][1]★$m{pet_c}を生贄にしました<br>"; &remove_pet;} ],
	18 => ['ﾛｷを生贄+戦争勝利数500以上',			sub{ ($pets[$m{pet}][0] eq '12' && $m{win_c}>=500) },	sub{$mes.="$pets[$m{pet}][1]★$m{pet_c}を生贄にしました<br>"; &remove_pet;} ],
);


#=================================================
sub begin {
	if ($m{tp} > 1) {
		$mes .= '他に何かありますか?<br>';
		$m{tp} = 1;
	}
	else {
		$mes .= "ここでは$m{name}の持っている勲章に応じて部隊をｸﾗｽﾁｪﾝｼﾞしたりできます<br>";
		$mes .= 'どうしますか?<br>';
	}
	&menu('やめる','お金が欲しい','ｱｲﾃﾑが欲しい','部隊を変えたい','名誉職になる','自分だけの武器が欲しい','勲章が欲しい');
}
sub tp_1 {
	return if &is_ng_cmd(1..6);
	$m{tp} = $cmd * 100;
	&{ 'tp_'. $m{tp} };
}

#=================================================
# 勲章→お金
#=================================================
sub tp_100 {
	$layout = 1;
	$m{tp} += 10;
	$mes .= "$m{name}の所持している勲章は$m{medal}個ですね<br>";
	$mes .= "勲章1個につき $exchange_money Gに換えることができます<br>";
	$mes .= "何個の勲章を献上しますか?<br>";
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="text" name="medal" value="0" class="text_box1" style="text-align:right">個|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="献上する" class="button1"></p></form>|;
}
sub tp_110 {
	if ($in{medal} && $in{medal} !~ /[^0-9]/) {
		if ($in{medal} > $m{medal}) {
			$mes .= "$in{medal}個も勲章を持っていません<br>";
		}
		else {
			my $v = $in{medal} * $exchange_money;
			$m{money} += $v;
			$m{medal} -= $in{medal};
			
			$mes .= "勲章$in{medal}個を献上して $v Gをもらいました<br>";
		}
	}
	&begin;
}

#=================================================
# 勲章→ｱｲﾃﾑ
#=================================================
sub tp_200 {
	$layout = 1;
	$m{tp} += 10;
	$mes .= "$m{name}の所持している勲章は$m{medal}個ですね<br>";
	$mes .= "どれと交換しますか?<br>";
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<table class="table1" cellpadding="3"><tr><th>名前</th><th>勲章<br></th></tr>|;
	$mes .= qq|<tr><td colspan="2"><input type="radio" name="cmd" value="0" checked>やめる<br></td></tr>|;
	for my $i (1 .. $#prizes) {
		$mes .= qq|<tr><td><input type="radio" name="cmd" value="$i">|;
		$mes .= $prizes[$i][0] eq '1' ? qq|[$weas[ $prizes[$i][1] ][2]]$weas[ $prizes[$i][1] ][1]</td>|
			  : $prizes[$i][0] eq '2' ? qq|[卵]$eggs[ $prizes[$i][1] ][1]</td>|
			  : $prizes[$i][0] eq '3' ? qq|[ペ]$pets[ $prizes[$i][1] ][1]</td>|
			  : 						qq|[$guas[ $prizes[$i][1] ][2]]$guas[ $prizes[$i][1] ][1]</td>|
			  ;
		$mes .= qq|<td align="right">$prizes[$i][2]個<br></td></tr>|;
	}
	$mes .= qq|</table>|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p>×<input type="text" name="loop" value="1" class="text_box1" style="text-align:right"></p>|;
	$mes .= qq|<p><input type="submit" value="交換する" class="button1"></p></form>|;
}
sub tp_210 {
	if ($cmd && defined $prizes[$cmd]) {
		if ($in{loop} && $in{loop} !~ /[^0-9]/) {
			for my $loop (1..$in{loop}) {
				if ($m{medal} >= $prizes[$cmd][2]) {
					$m{medal} -= $prizes[$cmd][2];
					
					$mes .= "勲章$prizes[$cmd][2]個を献上して";

					if ($prizes[$cmd][0] eq '1') {
						$mes .= "$weas[ $prizes[$cmd][1] ][1]に交換しました<br>";
						&send_item($m{name}, $prizes[$cmd][0], $prizes[$cmd][1], $weas[ $prizes[$cmd][1] ][4], 0, 1);
					}
					elsif ($prizes[$cmd][0] eq '2') {
						$mes .= "$eggs[ $prizes[$cmd][1] ][1]に交換しました<br>";
						&send_item($m{name}, $prizes[$cmd][0], $prizes[$cmd][1], 0, 0, 1);
					}
					elsif ($prizes[$cmd][0] eq '3') {
						$mes .= "$pets[ $prizes[$cmd][1] ][1]に交換しました<br>";
						&send_item($m{name}, $prizes[$cmd][0], $prizes[$cmd][1], 0, 0, 1);
					}
					elsif ($prizes[$cmd][0] eq '4') {
						$mes .= "$guas[ $prizes[$cmd][1] ][1]に交換しました<br>";
						&send_item($m{name}, $prizes[$cmd][0], $prizes[$cmd][1], 0, 0, 1);
					}
				}
				else {
					$mes .= '勲章が足りません<br>';
				}
			}
		}
	}
	&begin;
}

#=================================================
# 勲章→部隊＋お金
#=================================================
sub tp_300 {
	$m{tp} += 10;
	$mes .= "$m{name}の所持している勲章は$m{medal}個ですね<br>";
	$mes .= "ｸﾗｽﾁｪﾝｼﾞで余った勲章はお金に換金します<br>";
	$mes .= "どの部隊にｸﾗｽﾁｪﾝｼﾞしますか?<hr>";
	$mes .= "今の部隊からでｸﾗｽﾁｪﾝｼﾞできるのは以下です<br>";
	
	$mes .= "$units[0][1] 条件：なし<br>";
	my @menus = ('やめる', $units[0][1]);
	if ($config_test) {
		for my $i (1 .. $#units) {
			$mes .= "$units[$i][1] 条件：なし<br>";
			push @menus, $units[$i][1];
		}
	}
	else {
		for my $i (1 .. $#units) {
			if ($i eq $units[$m{unit}][2]) {
				$mes .= "$units[$i][1] 条件：なし<br>";
				push @menus, $units[$i][1];
			}
			elsif ($m{unit} eq $units[$i][2]) {
				$mes .= "$units[$i][1] 条件：$units[ $units[$i][2] ][1]/勲章$units[$i][3]個/";
				$mes .= $plus_needs{$i}[0] if defined $plus_needs{$i};
				$mes .= "<br>";
				
				push @menus, $units[$i][1];
			}
			else {
				push @menus, '';
			}
		}
	}
	
	&menu(@menus);
}
sub tp_310 {
	if ($cmd) {
		--$cmd;

		if ($cmd) {
			if ($config_test) {
				$m{unit} = $cmd;
				$mes .= "$units[$m{unit}][1]にｸﾗｽﾁｪﾝｼﾞしました<br>";
				&begin;
				return;
			}

			# ｸﾗｽﾀﾞｳﾝ
			unless ($cmd eq $units[$m{unit}][2]) {
				# 特殊条件
				if (defined $plus_needs{$cmd}) {
					if (&{ $plus_needs{$cmd}[1] } && $units[$cmd][2] eq $m{unit} && $m{medal} >= $units[$cmd][3]) {
						&{ $plus_needs{$cmd}[2] };
						$m{medal} -= $units[$cmd][3];
					}
					else {
						$mes .= "ｸﾗｽﾁｪﾝｼﾞできる条件を満たしていません<br>";
						&begin;
						return;
					}
				}
				elsif ($units[$cmd][2] eq $m{unit} && $m{medal} >= $units[$cmd][3]) {
					$m{medal} -= $units[$cmd][3];
				}
				else {
					$mes .= "ｸﾗｽﾁｪﾝｼﾞできる条件を満たしていません<br>";
					&begin;
					return;
				}
			}
		}
		
		$m{unit} = $cmd;
		$mes .= "$units[$m{unit}][1]にｸﾗｽﾁｪﾝｼﾞしました<br>";

		if ($m{medal} > 0) {
			my $v = $m{medal} * $exchange_money;
			$m{money} += $v;
			$mes .= "残りの勲章$m{medal}個を献上して $v Gをもらいました<br>";
			$m{medal} = 0;
		}
	}
	&begin;
}

#=================================================
# 名誉職
#=================================================
sub tp_400 {
	if ($m{rank_exp} <= 6210 || $m{rank} != $#ranks) { # (13*13*10) + (14*14*10) + (16*16*10) かつ 最高階級時
		$mes .= "名誉階級になれる条件を満たしていません<br>";
		&begin;
		return;
	}

	$layout = 1;
	$m{tp} += 10;
	$mes .= "1世代限りの名誉職に就きます<br>";
	$mes .= "貢献値2560で階級名を自由に変えられます<br>";
	$mes .= "名誉職になりますか?<br>";
	
	$mes .= qq|<form method="$method" action="$script">|;
	$mes .= qq|<input type="text" name="s_rank" value="" class="text_box1" style="text-align:right">階級名|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|<p><input type="submit" value="名誉職になる" class="button1"></p></form>|;
}
sub tp_410 {
	&error("階級名が長すぎます全角5(半角10)文字までです") if length $in{s_rank} > 10;
	if ($in{s_rank}) {
		$m{rank_exp} -= 2560;
		$m{super_rank} += 1;
		$in{s_rank} =~ s/★/☆/g;
		$m{rank_name} = $in{s_rank};

		$mes .= "名誉職「★$m{rank_name}」になりました<br>";
	}
	&begin;
}

#=================================================
# 宝具
#=================================================
sub tp_500 {
	$m{tp} += 10;
	$mes .= "ｸﾛﾑﾊｰﾂかｻﾃﾗｲﾄと引き換えに自分の武器を見つけます<br>";
	&menu('やめる','武器を捧げる');
}
sub tp_510 {
	if ($cmd eq '1' && $m{wea} eq '32,36' && $m{wea_lv} >= 30) {
		$mes .= "ﾍﾟｯﾄを送りました<br>";
		$m{wea} = $m{wea_c} = $m{wea_lv} = 0;
		&send_item($m{name}, 3, 191, 0, 0, 1);
	}else{
		$mes .= "★30のｸﾛﾑﾊｰﾂかｻﾃﾗｲﾄと交換できます<br>";
	}
	&begin;
}

#=================================================
# 武器→勲章
#=================================================
sub tp_600 {
	$m{tp} += 10;
	$mes .= "$m{name}の所持している勲章は$m{medal}個ですね<br>";
	$mes .= "ご愛用の武器を勲章 $exchange_medal 個に換えることができます<br>";
	$mes .= "売り払いますか?<br>";
	
	&menu('やめる','売り払う');
}
sub tp_610 {
	if ($cmd eq '1') {
		if ($m{wea_lv} ne '30') {
			$mes .= "新品では勲章に変えられません<br>";
		}
		else {
			$m{wea} = 0;
			$m{wea_c} = 0;
			$m{wea_lv} = 0;
			if($m{wea_name}){
				$m{wea_name} = "";
				$exchange_medal += 0;
			}
			$m{medal} += $exchange_medal;
			
			$mes .= "愛用の武器を質に入れ、勲章を $exchange_medal 個もらいました<br>";
		}
	}
	&begin;
}


1; # 削除不可

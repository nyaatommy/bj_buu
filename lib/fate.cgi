use List::Util;
my $this_file = "$userdir/$id/super.cgi";
#=================================================
# �p�Y
# ��Ԏ��Ă���ّ���Ƃ̑傫�ȈႢ�́A�߯Č��ʂ���������܂ŕ�����Ȃ����A��������O�ɕ������Ă��邩�̈Ⴂ
# �ّ��ƍ������Ⴆ�΂Ǝv���C������}���Ėʔ��������o���̂Ȃ�΁A
# �e��ڲ԰�ł��ꂼ��b�������Z�����߂ĊȒP�����ǎア�K�E�Z���������ǋ����K�E�Z�ւƂ��܂��q����Ζʔ������Ȃ݂�����
# ��ēʂ͏W�c�푈�����ǁA����̕K�E�Z�ł݂����Ȃ̂ɂȂ�Ηǂ��ȂƎv���Ď������Ă���
#=================================================
# ��p����
# 6���Ԃ���3���ԂɒZ�k ��ł��̎��Ԃ�����Z�k������ 0 �ɂ���͔̂������ĂȂ��]�X�����ɉB���K�E�Z�_���₷���Ȃ邾��
# �P���ɊԊu�Z�����������܂��}�V �S�̓I�ɕK�E�Z����l�����Ȃ����C�����Ȃ��ł��Ȃ��̂Ŕ{���ĂĂ����Ȃ��C������̂Ŕ�����
$coolhour = $config_test ? 0 : 3;
$cooldown_time = $coolhour * 3600;
=pod
���؎I�̎d�l
# �g���K�[
@triggers = (
#	[0]No	[1]���O			[2]type			[3]�{��	[4]�I���\	[5]������(%)
	[0,		'ϲٰ�',		'myroom',		0.1,	1,			100],
	[1,		'�푈����',		'war',			0.5,	1,			100],
	[2,		'�R������',		'military',		0.4,	1,			60],
	[3,		'�U�v����',		'breakdown',	1,		0,			100],
	[4,		'�O�𐬌�',		'promise',		0.4,	1,			60],
	[5,		'���z��',		'declaration',	0.8,	0,			80],
	[6,		'�����',		'cessation',	0.6,	0,			80],
	[7,		'����',			'domestic',		0.4,	1,			50],
	[8,		'�퓬����',		'battle',		0.3,	0,			20],
	[9,		'�C�s',			'training',		0.4,	0,			30],
	[10,	'����',			'hunting',		0.4,	0,			30],
	[11,	'���Z��',		'colosseum',	0.4,	0,			80],
	[12,	'��R�ł�',		'single',		1,		0,			100],
	[13,	'����',			'casino',		0.2,	0,			1],
	[14,	'����',			'voice',		0.2,	0,			10],
	[15,	'�z��',			'incubation',	0.3,	0,			100],
	[16,	'�E��',			'prison',		0.5,	0,			100],
	[17,	'�~�o',			'rescue',		0.7,	0,			70],
	[18,	'���Z��D��',	'colosseum_top',1,		0,			100],
	[19,	'�{�X����',		'boss',			1,		0,			100],
	[20,	'�\��',			'random',		1,		0,			100],
);
=cut

# ������ƒ�グ
# �g���K�[
@triggers = (
#	[0]No	[1]���O			[2]type			[3]�{��	[4]�I���\	[5]������(%)
	[0,		'ϲٰ�',		'myroom',		0.15,	1,			100],
	[1,		'�푈����',		'war',			0.7,	1,			100],
	[2,		'�R������',		'military',		0.6,	1,			60],
	[3,		'�U�v����',		'breakdown',	1.3,		0,			100],
	[4,		'�O�𐬌�',		'promise',		0.5,	1,			60],
	[5,		'���z��',		'declaration',	0.9,	0,			80],
	[6,		'�����',		'cessation',	0.8,	0,			80],
	[7,		'����',			'domestic',		0.5,	1,			50],
	[8,		'�퓬����',		'battle',		0.3,	0,			20],
	[9,		'�C�s',			'training',		0.4,	0,			30],
	[10,	'����',			'hunting',		0.4,	0,			30],
	[11,	'���Z��',		'colosseum',	0.4,	0,			80],
	[12,	'��R�ł�',		'single',		1,		0,			100],
	[13,	'����',			'casino',		0.2,	0,			1],
	[14,	'����',			'voice',		0.2,	0,			10],
	[15,	'�z��',			'incubation',	0.3,	0,			100],
	[16,	'�E��',			'prison',		0.75,	0,			100], # Ӽӂœ�������邯�ǈ���ڂŒE���ł���Ƃ͌���Ȃ��������Ō����ΐ푈�̂��܂������ȒP���������ǂ������͕�������Ȃ� �Ƃ͂����N�ł�Ӽӎ����Ă�󂶂�Ȃ����푈��肿����ƍ��߂�
	[17,	'�~�o',			'rescue',		1,	0,			100], # Ӽӂœ��������ċ~�o�Ŕ��������Ǔ�l���̍S�����K�v�ɂȂ邵������100%�ɂ��Č��ʗʂ��グ��i�푈2��ɂ͗�邯�ǐ푈�ɎQ���ł��Ȃ��l��ӼӍs�����Đ푈�ŋ~�o�݂����ȁj
	[18,	'���Z��D��',	'colosseum_top',1,		0,			100],
	[19,	'�{�X����',		'boss',			1,		0,			100],
	[20,	'�\��',			'random',		1,		0,			100],
);

=pod
# �������ɔ����ł���悤�ɂ��ăg���K�[�̔��������C�W��Ȃ� �����ĂȂ�
# �g���K�[
@triggers = (
#	[0]No	[1]���O			[2]type			[3]�{��	[4]�I���\	[5]������(%)
	[0,		'ϲٰ�',		'myroom',		0.1,	1,			100],
	[1,		'�푈����',		'war',			0.5,	1,			20],
	[2,		'�R������',		'military',		0.4,	1,			15],
	[3,		'�U�v����',		'breakdown',	1,		0,			100],
	[4,		'�O�𐬌�',		'promise',		0.4,	1,			12],
	[5,		'���z��',		'declaration',	0.8,	0,			30], # ���ƈ���Ĕ\���I�ɕz���ł��邩���� �����ƒႭ�Ă��ǂ����������ǓK���œ����邩��
	[6,		'�����',		'cessation',	0.6,	0,			60], # �z���ƈ���Ď󓮓I������z����荂��
	[7,		'����',			'domestic',		0.4,	1,			10],
	[8,		'�퓬����',		'battle',		0.3,	0,			20],
	[9,		'�C�s',			'training',		0.4,	0,			30],
	[10,	'����',			'hunting',		0.4,	0,			30],
	[11,	'���Z��',		'colosseum',	0.4,	0,			80],
	[12,	'��R�ł�',		'single',		1,		0,			100],
	[13,	'����',			'casino',		0.2,	0,			1],
	[14,	'����',			'voice',		0.2,	0,			10],
	[15,	'�z��',			'incubation',	0.3,	0,			100],
	[16,	'�E��',			'prison',		0.5,	0,			100],
	[17,	'�~�o',			'rescue',		0.7,	0,			70],
	[18,	'���Z��D��',	'colosseum_top',1,		0,			100],
	[19,	'�{�X����',		'boss',			1,		0,			100],
	[20,	'�\��',			'random',		1,		0,			100],
);
=cut

=pod
# ���؎I�ł̎d�l
# �^�C�~���O
@timings = (
#	[0]No	[1]���O							[2]����		[3]�{��		[4]�I���\
	[0,		'�C��',							sub{ return 1; },	0.1,	1],
	[1,		'�ŖS��',						sub{ return $cs{is_die}[$m{country}]; },	0.5,	1],
	[2,		'����į��',					sub{ for my $i (1..$w{country}) { if ($cs{strong}[$i] > $cs{strong}[$m{country}]) { return 0; } } return 1; },	0.7,	0],
	[3,		'���������ׂ�100000�����̎�',	sub{ return ($cs{food}[$m{country}] < 100000 && $cs{money}[$m{country}] < 100000 && $cs{soldier}[$m{country}] < 100000); },	0.4,	1],
	[4,		'���m��20000�����̎�',			sub{ return $cs{soldier}[$m{country}] < 20000; },	0.6,	0],
	[5,		'���m��999999�̎�',				sub{ return $cs{soldier}[$m{country}] >= 999999; },	0.8,	0],
	[6,		'��\�̎�',						sub{ return &is_daihyo; },	0.3,	1],
);
=cut

=pod
�S�̓I�ɏI�ՓD�����������ȋC������

��{�Ƃ��đ�\�͊e���Œ�4�l���������݂��Ă���A��ēʂő�\���z�������悤�ɑ�\�����Ŏn�܂葼�̏����Ɍq���Ă����̂����z�Ǝv���Ă���
��\�̎�������߰���ŖS����


�V�i�W�[
�����g�ށ������������鎞
������߰(ɱ)���ŖS��
����0�ŖS���ŖS���E����0����������߰(����+1)������1���E���Ϳ�ۖڎ�
����0�ŖS���ŖS���E����0�������ފo�����e�E�߯Ă̳��ށ����Ϳ�ۖڎ�
����0�ŖS���ŖS���E����0��������������Ϳ�ۖڎ��i����+0�`100�Ȃ̂�1�E11�E22�E33�E44�E55�E66�E77�E88�E99�������邩������Ȃ��B������Ȃ��Ăസ����߰����+1�Ŕ������ł���B̪��ٖW�Q���邯�ǁj
���ށ����ފo����
������߰(����+1)������%50�E���Ϳ�ۖ�
������߰(��Փx+1)������%5
�޳�������%12�E����%3
̪��ف�����%3
����ݸ���O�����ꎞ
����(��������)��FMS<10��
����(�����Փx-1)������%5
������ް(�^�ŖS)���ŖS��
������ް(����0)������0��
������ް(��ԕύX)���\���E�s����
������ް(��Փx�㏸)������%5

���ʗ�
������ۖ�		4			�I����
���Ϳ�ۖ�		3			�I��s��		�Ӑ}���Ă�Ƃ͂�������ƴ�����߰�Ƃ��I�ՈӊO�Ƒ_���� �{��4����3�Ɍ��炵�đI��s�ɕύX ����ɓ��ꍑ�Ϳ�ۖڂ�ǉ�
����1				2			�I����		����1���@�\��������ƎO���u�݂����ɓD���ɂȂ肻���ȗ\��������̂Ŕ{��3����2�Ɍ��炵��
�ڂ���			1.25		�I��s��
�E���{			1.2		�I����		���ގ��̂��������炳��ɏ����ɉ�����Ƌ����H
����0				1			�I��s��
�g�b�v			0.7		�I��s��
��%5			0.62		�I����		������ӂ̔{���ł��I�����~�����Ǝv����
SOL<2��			0.6		�I��s��
SOL��				0.6		�I��s��
����%3			0.6		�I��s��
����%5			0.43		�I����
FMS<10��			0.4		�I����
�O������			0.38		�I��s��
�ŖS��			0.35		�I����
�r��				0.34		�I����
��\��			0.32		�I����
��>4			0.28		�I����
�Ɛg��			0.27		�I����
�\�E�s			0.26		�I����
����%12			0.25		�I����
����%7			0.25		�I����
������			0.212		�I����
�C��				0.1		�I����
=cut

# �R�s�y�Ȃ̂ŗv��Ȃ��f�[�^�����Ă邯�ǂ܂��d�l�����܂��ĂȂ��̂ŕ��u
# �R���Z�v�g�Ƃ��č��֌W�������Ɍ��肵�Ă���ۂ����ǔ��������ɂ������Ă��ƂŊɘa���č��Ɋ֌W�Ȃ����������Ȃ�ǉ������i�Ɛg�̎���A���񐔂⃌�x���Ȃǁj
# �^�C�~���O
$timing_base = 0; # 0.2 # �������Ŕ����Ȃ� 0 �𒴂��鐔�l ���̐��l���������������̃x�[�X�{���ƂȂ�
@timings = (
#	[0]No	[1]���O							[2]����		[3]�{��		[4]�I���\
	[0,		'�C��',								sub{ return 0.1; },	0.1,	1],
	[1,		'�ŖS��',							sub{ return $cs{is_die}[$m{country}] ? 0.35 : $timing_base; },	0.5,	1],
	[2,		'�����������鎞',					sub{ return $union ? 0.212 : $timing_base; },	0.12,	1], # �ڂ����Ɠ������̎d�l�t���܂ɂ��� �������Ȃ��ōςށu������g�܂Ȃ��v�Ɍ���������u�����g�����v�Ƀo�C�A�X�|����
	[3,		'�ڂ����̎�',						sub{ return !$union ? 1.25 : $timing_base; },	0.12,	0], # ���͑I����0.212���������ǉB���ɂ��Č��ʍ���
	[4,		'����į�߂̎�',					sub{ for my $i (1..$w{country}) { if ($cs{strong}[$i] > $cs{strong}[$m{country}]) { return $timing_base; } } return 0.7; },	0.7,	0], # �����L���̏����Ɠ����ŋt���܂ɂ��������ǂ������H ̪��ق͎����H���Ȃ����g�b�v���͈ێ��ȒP���낤����g�b�v2��̪��ِH�炤�Ńo�����X����Ă�Ǝv����
	[5,		'������؂̎�',						sub{ for my $i (1..$w{country}) { if ($cs{strong}[$i] < $cs{strong}[$m{country}]) { return $timing_base; } } return 0.34; },	0.7,	1], # �r���ڎw���Đ푈���Ȃ������g�b�v�ڎw���Đ푈����������S����
	[6,		'���Ϳ�ۖڂ̎�',					sub{ return ($cs{strong}[$m{country}] > 1 && $cs{strong}[$m{country}] =~ /^(\d)\1+$/) ? 3 : $timing_base; },	0.7,	0],
	[7,		'����1�̎�',						sub{ return ($cs{strong}[$m{country}] == 1) ? 2 : $timing_base; },	0.7,	1],
	[8,		'����0�̎�',						sub{ return ($cs{strong}[$m{country}] == 0) ? 1 : $timing_base; },	0.7,	0],
	[9,		'���͂� 12 �̔{���̎�',			sub{ return $cs{strong}[$m{country}] > 0 && (($cs{strong}[$m{country}] % 12) == 0) ? 0.25 : $timing_base; },	0.7,	1],
	[10,		'�\���E�s���̎�',					sub{ return ($cs{state}[$m{country}] == 3 || $cs{state}[$m{country}] == 4) ? 0.26 : $timing_base; },	0.7,	1],
	[11,		'����۽�o����',					sub{ return ($cs{extra}[$m{country}] > 0 && $cs{extra_limit}[$m{country}] >= $time) ? 1.2 : $timing_base; },	0.7,	1],
	[12,		'���������ׂ�100000�����̎�',	sub{ return ($cs{food}[$m{country}] < 100000 && $cs{money}[$m{country}] < 100000 && $cs{soldier}[$m{country}] < 100000) ? 0.4 : $timing_base; },	0.4,	1],
	[13,		'���m��20000�����̎�',			sub{ return $cs{soldier}[$m{country}] < 20000 ? 0.6 : $timing_base; },	0.6,	0],
	[14,		'���m��999999�̎�',				sub{ return $cs{soldier}[$m{country}] >= 999999 ? 0.6 : $timing_base; },	0.8,	0],
	[15,		'��\�̎�',							sub{ return &is_daihyo ? 0.32 : $timing_base; },	0.3,	1],
	[16,		'�Ɛg�̎�',							sub{ return $m{marriage} ? $timing_base : 0.27; },	0.3,	1],
	[17,		'�A��5��ȏ�̎�',				sub{ if ($m{renzoku_c} > 4) { $m{renzoku_c} = 0; return 0.28; } else { return $timing_base; } },	0.3,	1],
	[18,		'�A���񐔂� 5 �̔{���̎�',		sub{ return ($m{renzoku_c} > 0 && ($m{renzoku_c} % 5) == 0) ? 0.62 : $timing_base; },	0.3,	0], # �{���L�b�J���Ȃ̂Ŕ��������Ǝ��̔{���܂ł��a��
	[19,		'���ꍑ�͂� 3 �̔{���̎�',		sub{ return ($touitu_strong % 3) == 0 ? 0.6 : $timing_base; },	0.3,	0], # 3 ���Ɠ�����₷�߂��H 4 �Ƃ� 6 ���炢�ɂ��Ă���������̪��فE�޳��ŃK�N�K�N���� ����
	[20,		'���ꍑ�͂���ۖڂ̎�',			sub{ return ($touitu_strong > 1 && $touitu_strong =~ /^(\d)\1+$/) ? 4 : $timing_base; },	0.7,	1],
	[21,		'�����Փx�� 5 �̔{���̎�',	sub{ return ($w{game_lv} % 5) == 0 ? 0.43 : $timing_base; },	0.3,	1],
	[22,		'�O�����ꍑ�̎�',					sub{ my($c1, $c2) = split /,/, $w{win_countries}; return ($c1 == $m{country} || $c2 == $m{country}) ? 0.38 : $timing_base; },	0.3,	0],
	[23,		'���ق� 7 �̔{���̎�',			sub{ return $m{lv} % 7 == 0 ? 0.25 : $timing_base; },	0.3,	1],

# �ϓ����Â炢�̂ŃC�}�C�`
#	[16,		'�d�����g�b�v',					sub{ for my $i (1..$w{country}) { if ($cs{member}[$i] > $cs{member}[$m{country}]) { return 0.2; } } return 0.5; },	0.7,	1],
#	[17,		'�d�����r��',					sub{ for my $i (1..$w{country}) { if ($cs{member}[$i] < $cs{member}[$m{country}]) { return 0.2; } } return 0.5; },	0.7,	1],
);


=pod
�l�I�ɂ͏������E��݃f�����b�g�݂������[�U�[���f�����b�g�̋����ς����鍀�ڂ������Ɨ~����
�u�[�X�g����������͂�����Ηǂ����A�f�����b�g�����Ȃ�u�[�X�g�����Ȃ���Ηǂ����݂�����
���͌������������Ȃ��Ƃ� ���������v�Z�ɂ�������Ă����̂�������N�������ė~����
�߯ăf�����b�g�͂قƂ�ǎ����ĂȂ����ǂƂ�ł��Ȃ����ƂɂȂ邩��

���ʗ�
�S�~�N�Y		4					2.6���`260������ 100����܂ŏオ�葱���镾�Q�ŗ�������������S�~�N�Y�̎d�l�����ɖ߂��Ƃ�������
������		3					���������Ȃ͕̂������Ă邵�w�E������������Ȃ񂩂��������ǂ����� ���޳݂̌����ł� 2 �������x�� +5 �̃X�e�����Ȃ��ɂ��� 3 ���炢�ł��ǂ����� �ł������������莩�̂�����
�߯�����		�R�[�h�Q��		��7�Ԃ������2.6
����			2.3				+24���ԂŐݒ肵�Ă����ǂƂ�ł��Ȃ��g���ɂ������� +6���Ԃŉ��X�������ԐL�т邯����׳���قŋ������ԃ`�����ɂȂ�\������
no1�n��		2.2				�����đ����Ă��قƂ�ǖ�肪�Ȃ���ɏオ��ɂ����n���Ȃ̂ł����Ă�
���޳�		2					9����X�e��1��-19�`0�����債�����ƂȂ� ������
����			1.6				��������دĂ���Ȃ��Ȃ�\�������邯�Ǒ債�����ƂȂ����H
��������		1.6				���دĂ���Ȃ��Ƃ������邵�ެݸ�ŃS�~���픃���Ēb���Ďg���Ă����܂����Ǔ�������Ă��Ƃ�
�M��			1.2				10���5���3����ɕύX ��ڂ����邵5���ǂ������H
�z���l		1.2				�z���l-100��������׳���قśz���l+300�Ƃ������Ⴆ�Α����}������ ��ĉ��ŗa�����ςȂ��ŖY��Ă��̂Ƃ��f�����b�g�Ȃ��Ɏg����
�S��			1
�v���l		1					��ڲ԰�ɂƂ��Ă͒ɂ����y�����Ȃ� ���ԂƂ�����ΓI���l�ƒނ荇�����̂ł͂Ȃ����Ǔ�����Ƃ���
������		0.75�`3.249�H	�����������قǃu�[�X�g
������2		0.7
���			0.65�`1.9�H		��ݑ����قǃu�[�X�g
���2			0.6
�Ȃ�			0.5

�z���l		0.5�`�z���l * 0.006		��ĉ���ʽ�ڴ��ނԂ����ޗp �z�����݂Ԃ������ 59.99400 �C�����ˁI
=cut
# ���̑��f�����b�g
$demerit_base = 0.5; # �������Ŕ����Ȃ� 0 �𒴂��鐔�l ���̐��l���������������̃x�[�X�{���ƂȂ�
@demerits = (
#	[0]No	[1]���O				[2]�f�����b�g		[3]�{��		[4]�I���\
	[0,		'�Ȃ�',				sub{ return $demerit_base; },		0.5,	0],
	[1,		'��{�S��',			sub{ &wait; return 1; },	1,	1],
	[2,		'������',			sub{ $m{lv} = 99; $m{exp} = 100; return 3; },	1.2,	0],
	[3,		'�ð���޳�',	sub{ @st = (qw/max_hp max_mp at df mat mdf ag cha lea/); $k = $st[int(rand(@st))]; $m{$k} -= int(rand(20)); $m{$k} = $m{$k} <= 0 ? int(rand(20)):$m{$k}; return 2; },	1.2,	0],
	[4,		'�v���l100����',		sub{ $m{rank_exp} -= 100; return 1; },	1,	1],
#	[5,		'�v���l100����(��)',		sub{ $m{rank_exp} -= 100; return 0.8; },	0.8,	0],
	[5,		'������10%����',		sub{ if ($m{money} > 4999999) { my $vv = 4999999 * 0.0000005; $m{money} -= int(4999999 * 0.1); return $vv > 0 ? $vv + 0.75 : $demerit_base; } else { my $vv = $m{money} * 0.0000005; $m{money} = int($m{money} * 0.9); return $vv > 0 ? $vv + 0.75 : $demerit_base; } },	0.7,	1], # �ϰ�ެ��޾޳��ňꔭ�ŏI��邩�炠�Ƃōl����
	[6,		'������10000����',		sub{ $m{money} -= 10000; return 0.7; },	0.7,	0],
	[7,		'�M��3�ԏ�',		sub{ if (3 <= $m{medal}) { $m{medal} -= 3; return 1.2; } else { return $demerit_base; } },	1.5,	1],
#	[8,		'�M��10�ԏ�(��)',		sub{ $m{medal} -= 10; return 1; },	1,	0],
	[8,		'���10%����',		sub{ my $vv = $m{coin} * 0.0000005; $m{coin} = int($m{coin} * 0.9); return $vv > 0 ? $vv + 0.65 : $demerit_base ; },	0.8,	1],
	[9,		'���10000����',		sub{ if ($m{coin} > 9999) { $m{coin} -= 10000; return 0.6; } else { return $demerit_base; } },	0.5,	0],
	[10,		'���^+6����',		sub{ $m{next_salary} += int( 3600 * 6 ); return 2.3; },	1.4,	1],
	[11,		'�z���l100����',		sub{ if ($m{egg_c} > 99) { $m{egg_c} -= 100; return 1.2; } else { return 0.5; } },	0.6,	1], # �z���lؾ�Ă̏C���� �Œ�ɂ��đ�l����
	[12,		'��������-1',		sub{ if ($m{wea_lv} > 0) { $m{wea_lv} -= 1; return 1.6 } else { return 0.5; } },	0.6,	0],
	[13,		'�߯�����-1',		sub{ if ($m{pet_c} > 0) { my @fib_rets = (1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 2000, 5000, 10000, 20000, 50000, 100000); my $vv = $m{pet_c}; $m{pet_c}--; return 0.1 * $fib_rets[$vv] + 0.5; } else { return 0.5; } },	0.6,	0],
	[14,		'no1�n��-1',		sub{ if ($m{no1_c} > 0) { my $vv = $m{no1_c}; $m{no1_c} -= 1; return 2.2; } else { return 0.5; } },	0.6,	1],
	[15,		'�S�~�N�Y',			sub{ if ($m{shogo} ne $shogos[1][0]) { $m{shogo} = $shogos[1][0]; return 4; } else { return 0.5; } },	2.0,	0], # 2.6���`260������ 100����܂ŏオ�葱���镾�Q�ŗ�������������S�~�N�Y�̎d�l�����ɖ߂��Ƃ�������
	[16,		'����',			sub{ if ($m{marriage} ne '') { $m{marriage} = ''; return 1.6; } else { return 0.5; } },	1.5,	0], # 

#	[11,		'�z���lؾ��',		sub{ my $vv = $m{egg_c} * 0.006; $m{egg_c} = 0; return $vv + 0.5; },	0.6,	1], # �p��
);

# ��
@max_counts = (
#	[0]No	[1]��	[2]�{��	[3]�I���\
	[0,		1,		1,		1],
	[1,		2,		0.4,		0],
	[2,		3,		0.2,		0],
);

# �����̃u�������傫���ƃu�����̏������{���ɑ΂��ė������v�Z���ʂ̑������߂Ă��܂��i�{���̈Ӌ`�����܂�j
# �����I��global���ĂȂ����ǔz����̊֐��̃O���[�o���ϐ��ɊO����A�N�Z�X�ł��Ȃ��i�z�񂪒�`����Ċ֐����Ăяo���܂Ŋ֐�����`���ꂸ�O���[�o���ϐ��Ƃ��ċ@�\���Ȃ��݂����ȁH�j
# �Q�Ƃł��Ȃ�����֐����Ń��b�Z�[�W��Ԃ��悤�Ɏd�l�ύX
# ����
@effects = (
#	[0]No	[1]���O				[2]����			[3]�I���\	[4]���b�Z�[�W
	[0,		'̪���',			sub{
		$v = shift;
		$c = &get_most_strong_country;
		my ($attack_name, $attack_value) = get_attack_level(400);
		for my $i (1..$w{country}) {
			next if $i eq $m{country};
			next if $cs{strong}[$i] == 0; # ������߰�ō���1�Ɏ����čs�������̂ō���0�̍��̓X���[
#			$cs{strong}[$i] -= int((rand(16000)+2000) * $v);
#			$cs{strong}[$i] -= int((rand(16000)+2000) * $v) if ($i eq $c);

			$cs{strong}[$i] -= int($attack_value * (rand(0.1)+0.95) * $v);
			$cs{strong}[$i] -= int($attack_value * (rand(0.1)+0.95) * $v) if ($i eq $c); # ���̓g�b�v�ɂ�̪���2��
			if ($cs{strong}[$i] < 0) {
				$cs{strong}[$i] = int(rand(10)) * 100; # ���̓}�C�i�X�ɂȂ����獑�͂� 0�`900 ��
			}
		};
		&write_cs;
		return "$v�{$attack_name̪��قɂ���Ċe���̍��͂���������";
	},	1,	'̪��قɂ���Ċe���̍��͂���������'],
	[1,		'�޳�',				sub{
		$v = shift;
		# �����Ɠ�Փx�ɂ���邪̪���vs�޳����Ɗ�{̪��ق̂��g������ǂ������H
		# ̪��كQ�[���ǂ����Ǝv���̂ž޳�����グ���邩�������Ƀ����b�g�������Ă��ǂ�����
#		$v *= 1.5;
		my ($attack_name, $attack_value) = get_attack_level(1000);
#		$cs{strong}[$m{country}] += int((10000 + rand(10000)) * $v);
		$cs{strong}[$m{country}] += int($attack_value * $v);
		&write_cs;
		return "$v�{$attack_name�޳��ɂ����$c_m�̍��͂���������";
	},	1,	'�����̍��͂���������'],
	[2,		'���āi��n�k�j',				sub{
		$v = shift;
		$v *= 0.4;
#		my ($attack_name, $attack_value) = get_attack_level(100000);
		for my $i (1..$w{country}) {
			next if $i eq $m{country};
#			$cs{soldier}[$i] -= int((rand(600000)+200000) * $v);
#			$cs{soldier}[$i] = 0 if $cs{soldier}[$i] < 0;
			$cs{soldier}[$i] = int($cs{soldier}[$i] * 0.5 ** $v);
			$cs{soldier}[$i] = 0 if $cs{soldier}[$i] < 0;
		};
		--$w{game_lv} if int(rand(2)) < 1;
		&write_cs;
		return "$v�{���Ăɂ���đS���̕��m����������";
	},	0,	'�S���̕��m����������'], # 0
	[3,		'���āi���R�ЊQ�j',				sub{
		$v = shift;
		$v *= 0.4;
		for my $i (1..$w{country}) {
			next if $i eq $m{country};
#			$cs{food}[$i] -= int((rand(600000)+200000) * $v);
			$cs{food}[$i] = int($cs{food}[$i] * 0.5 ** $v);
			$cs{food}[$i] = 0 if $cs{food}[$i] < 0;
		};
		--$w{game_lv} if int(rand(2)) < 1;
		&write_cs;
		return "$v�{���Ăɂ���đS����$e2j{food}����������";
	},	0,	'�S���̐H�Ƃ���������'], # 0
	[4,		'���āi�o�ϔj�]�j',				sub{
		$v = shift;
		$v *= 0.4;
		for my $i (1..$w{country}) {
			next if $i eq $m{country};
#			$cs{money}[$i] -= int((rand(600000)+200000) * $v);
			$cs{money}[$i] = int($cs{money}[$i] * 0.5 ** $v);
			$cs{money}[$i] = 0 if $cs{money}[$i] < 0;
		};
		--$w{game_lv} if int(rand(2)) < 1;
		&write_cs;
		return "$v�{���Ăɂ���đS����$e2j{money}����������";
	},	0,	'�S���̎�������������'], # 0
	[5,		'�ٶ�׽�',				sub{
		# �ٶ�׽ނ����[�e�X�g�� ���؎I�d�l�̂����Ԃ�ア�񂾂Ǝv��
		# �{���\������̔{���Ǝ��ۂ̌��ʗʂ��Ⴄ����̔{���C�W�����֌W�ŐV�����d�l�ɂ��悤����
		$v = shift;
		my @ks = (qw/ceo war dom pro mil/);

=pod
		my @ks = (qw/war dom pro mil/);
		@ks = List::Util::shuffle(@ks);
		unshift @ks, 'ceo';
=cut

		my @ks2 = ();
		my $vv = $v - int($v);
		for my $i (0 .. int($v)) {
			my $k = $ks[int(rand(@ks))];
			next if int(rand(2)) < 1;
			if ((int($v)-$i) >= 1 || rand(1) < $vv) {
				push @ks2, $k;
			}
		}

		my %cnt;
		@ks2 = grep {!$cnt{$_}++} @ks2;

		unless (@ks2) {
			&write_cs;
			return "$v�{�ٶ�׽ނ͕s���ɏI�����";
		}

		my $daihyo = '';
		for my $k (@ks2) {
			$daihyo .= "$e2j{$k}";
		 	for my $i (1 .. $w{country}) {
	 			next if $cs{$k}[$i] eq '';
	 			next if $i eq $m{country};
#	 			next if rand(0.1) > $v;

	 			&regist_you_data($cs{$k}[$i], 'lib', 'prison');
	 			&regist_you_data($cs{$k}[$i], 'tp', 100);
	 			&regist_you_data($cs{$k}[$i], 'y_country',  $m{country});
	 			&regist_you_data($cs{$k}[$i], 'wt', $GWT * 60);
	 			&regist_you_data($cs{$k}[$i], 'act', 0);

	 			open my $fh, ">> $logdir/$m{country}/prisoner.cgi" or &error("$logdir/$m{country}/prisoner.cgi ���J���܂���");
	 			print $fh "$cs{$k}[$i]<>$i<>\n";
	 			close $fh;
	 		}
		};
		&write_cs;
		return "$v�{�ٶ�׽ނɂ���đS����$daihyo���ċւ��ꂽ";
	},	1,	'�S���̑�\���ċւ��ꂽ'],
	[6,		'�ٶ�׽�(��)',				sub{
		$v = shift;
		$c = &get_most_strong_country;
		my @names = &get_country_members($c);
	 	for my $name (@names) {
			$name =~ tr/\x0D\x0A//d;
		
			&regist_you_data($name, 'lib', 'prison');
			&regist_you_data($name, 'tp', 100);
			&regist_you_data($name, 'y_country',  $m{country});
			&regist_you_data($name, 'wt', $GWT * 60);
			&regist_you_data($name, 'act', 0);
		
			open my $fh, ">> $logdir/$m{country}/prisoner.cgi" or &error("$logdir/$m{country}/prisoner.cgi ���J���܂���");
			print $fh "$name<>$c<>\n";
			close $fh;
		};
		&write_cs;
		return "$cs{name}[$c]�̍������ċւ��ꂽ";
	},	0,	"$cs{name}[$c]�̍������ċւ��ꂽ"], # 0
	# �K�E���ĂƖŖS���e����è�ŕ���������т܂���C������
	# ���Ď�̉������ĕ����������ʂ��グ�Ă��ǂ��C�����邪���Ă͓K������ɑ΂��Ă������͑I�����������ȂƂ�
	# �Ƃ肠�����{��1.5�{��W����
	[7,		'����',				sub{
		$v = shift;
		$v *= 1.5;
		my ($attack_name, $attack_value) = get_attack_level(50000);
#		$cs{food}[$m{country}] += int((500000 + rand(2000000)) * $v);
		$cs{food}[$m{country}] += int($attack_value * $v);
		&write_cs;
		return "$v�{$attack_name�����ɂ����$c_m�̐H�Ƃ���������";
	},	1,	'�����̐H�Ƃ���������'],
	[8,		'��޽',				sub{
		$v = shift;
		$v *= 1.5;
		my ($attack_name, $attack_value) = get_attack_level(50000);
#		$cs{money}[$m{country}] += int((500000 + rand(2000000)) * $v);
		$cs{money}[$m{country}] += int($attack_value * $v);
		&write_cs;
		return "$v�{$attack_name��޽�ɂ����$c_m�̎�������������";
	},	1,	'�����̎�������������'],
	[9,		'�ٽ',				sub{
		$v = shift;
		$v *= 1.5;
		my ($attack_name, $attack_value) = get_attack_level(50000);
#		$cs{soldier}[$m{country}] += int((500000 + rand(2000000)) * $v);
		$cs{soldier}[$m{country}] += int($attack_value * $v);
		&write_cs;
		return "$v�{$attack_name�ٽ�ɂ����$c_m�̕��m����������";
	},	1,	'�����̕��m����������'],
	# 1���ԌŒ�ɖ߂��������ǂ������H
	# ���ދ����w�E����������1����1�{����30��1�{�ɒ����A�����15���x�[�X�ɂ��ėl�q�� ���܂蒷���Ԃ͌������Ȃ������̂�20���x�[�X��
	# ���ފo�����͏㏑���ł��Ȃ��悤�ɂȂ��Ă������������Ă����ʂȂ����Ǝ₵���̂ŏ�ɏ㏑��
	# �����Ԃ���������ɒZ���Ԃ������ƌ��ʒZ�k�����ǋ����w�E�������������ꂮ�炢�ł��傤�Ǘǂ������H
	[10,	'����۽',				sub{
		$v = shift;
		my $vv = int(20 * $v);
#		if ($cs{extra_limit}[$m{country}] < $time) {
			$cs{extra_limit}[$m{country}] = $time + 60 * $vv;
			$cs{extra}[$m{country}] = 1;
#		}
		&write_cs;
		return "$c_m�̒D���͂�$vv����������";
	},	0,	'�����̒D���͂���������'], # 0
	[11,	'����۽(�R��)',				sub{
		$v = shift;
		my $vv = int(20 * $v);
#		if ($cs{extra_limit}[$m{country}] < $time) {
			$cs{extra_limit}[$m{country}] = $time + 60 * $vv;
			$cs{extra}[$m{country}] = 2;
#		}
		&write_cs;
		return "$c_m�̌R���͂�$vv����������";
	},	0,	'�����̌R���͂���������'], # 0
	[12,	'�����',				sub{
		$v = shift;
		# �����Փx�̉����鲰���
		# �I���\�̴�����߰�𓱓������̂Ų���������ׂ��󋵂͑�����������5000�ȏ�ŖŖS���Ă邱�Ƃ������Ĳ�����O�ɏ���ɕ���������
		# ���ɉ��������b�g�������������ǂ������Ȋ����i�ŖS���̍���+0�`100���ʂ𑫂����͍̂���1�����𖞂������ŖS���̎ז�������Ƃ�����0�ŖS�������ɑł��Ԃ������ۖڂɂȂ�\�������邽�߁j
		for my $i (1..$w{country}) {
			if ($cs{is_die}[$i]) {
				$cs{strong}[$i] += int(rand(101));
				$cs{is_die}[$i] = 0;
				--$w{game_lv};
			}
		};
		&write_cs;
		return "�S�����������܂���";
	},	1,	'�S�����������܂���'],
	[13,	'سާ����',				sub{
		$v = shift;
		$c = &get_most_strong_country;
		my ($attack_name, $attack_value) = get_attack_level(1500);
#		my $vv = int((20000 + rand(20000)) * $v);
		my $vv = int($attack_value * (rand(0.1)+0.95) * $v);
		$vv = $cs{strong}[$c] if $cs{strong}[$c] < $vv;
		$cs{strong}[$c] -= $vv;
		$cs{strong}[$m{country}] += $vv - int(rand($vv*0.3)); # int($vv / 3) # ���ꍑ�͉����H ���ꍑ�͏���������̂ł������ɓ��ꍑ�͓����������ǂ�����
		&write_cs;
		return "$v�{$attack_nameسާ���݂ɂ����$cs{name}[$c]�̍��͂�D����";
	},	0,	"$cs{name}[$c]�̍��͂�D����"], # 0
	[14,	'������ް',				sub{
		$v = shift;
		# �ꍑ��̪��ُW���C�΂����K�E�Z
		# ���̑Ώۍ��̍��͂ɂ����̪��ى��\�����ɂ��Ȃ��ē��ꍑ�͂�����
		# �{���͎������������̓g�b�v�ɓ�����󂾂��ǌ��铝�ꍑ�͂���{�ō��l��@���o���̂�1�`4�����炢�������ŃQ�[�����I���i�p�Y���ňꔭ���Ă邩�ǂ����őz�肵�Ă�͂��j
		# �����ƌ����₷�����ė~�����Ƃ������ƂŁA��{�펞�ō��l��@���o���Ȃ��悤�Ɏ��������������_���Z���N�g�ɕύX
		# ����ɂ����ɏI��肷���Ȃ��悤�ɓ����Փx���グ��悤�ɂ����̂œ����Փx�̔{�������𖞂������肷�邩������Ȃ�
		# �i�������������œ�Փx������̂œ�Փx�グ�鏈������Ȃ��Ɠ��ꍑ�͂������Փx���K���K�������葱���Ă��܂��j
		# �\���E�s������������̂ŃC���[�K���ȖŖS���@�����Ə�ԕύX�񐔂����ꂾ�������Ă��܂������������ɂ����Ȃ�����������������܂܂ɂȂ�̂ŏ�ԕύX���Č�������
		# ������߰�̕��͍��͂�0�ɂȂ�i�{���ɖŖS�����j�󂶂�Ȃ�����Č����Ȃ��ėǂ� ���Ƃ�����S���Q�[�Ƃ���w�K�E�Z�߽Ēǉ����������ǂ�����
		my @cs2 = (1 .. $w{country});
		splice(@cs2, $m{country}-1, 1);
		$c = $cs2[int(rand(@cs2))]; # &get_most_strong_country;
		$w{game_lv} += int($cs{strong}[$c]*0.0002); # �Ώۍ��̍���5000���ɓ�Փx+1
		$cs{strong}[$c] = 0;
		$cs{is_die}[$c] = 1;
		$cs{state}[$_] = int(rand(@country_states)) for (1 .. $w{country});
		&write_cs;
		return "$cs{name}[$c]�ɐ����������";
	},	0,	"$cs{name}[$c]�ɐ����������"], # 0
	[15,	'������߰',				sub{
		$v = shift;
		# �U������ް�A������ް����̪��ٌ��ʂ������Ă݂������ꂾ�Ɨv�͓G����ɱ�𒣂���ʂɂȂ��Ă��܂��i����ɖŖS����������������j
		# ����������Ǝ����ɗL���ɂȂ�悤�Ɋm����ɱ�𒣂�ŖS�������������悤�ɕύX
		# �����Փx�ɂ��Ăʹ�����ް�Ɠ��l
		# ɱ���ʂ����ŖS�����{����1�����{�����Փx�����𑀍삷�邽�߂Ɏg�����肷��̂�z��

		$c = rand(100) < 60 ? $m{country} : # ��{�������ʂ��������őI�ׂ�K�E�Z�Ŏg������ǂ�����̂ŁA
				int(rand($w{country})+1); # �G���Ɍ��ʂ�^����f�����b�g�ɂȂ邱�Ƃ�����悤��

		my $is_die = $cs{is_die}[$c];
		$cs{is_die}[$c] = 1;

		++$cs{strong}[$m{country}]; # ����+1 ����0�ŖŖS�������Ɍ����Ԃ��΍���1�����𖞂����� �^���ǂ���΍��̓]���ڂ��L�蓾��

		# �K���オ�邾�Ɠ�Փx�����Ȃ���肾�낤����m���� �����̏����ɗ��ދZ����
		# 1/2��2/5�ɕύX
		++$w{game_lv} if $is_die == 0 && int(rand(5)) < 2;
		&write_cs;
		return "$cs{name}[$c]��ῂ����ɕ�܂ꂽ";
	},	1,	"$cs{name}[$c]�ɐ����������"],
	[16,	'����ݸ',				sub{
		$v = shift;
		# �O�����ꍑ�������ɂ���K�E�Z �������������ł��I �z���l���������ł��I �O����������𖞂���
		$w{win_countries} = $m{country};
		&write_cs;
		return "$cs{name}[$m{country}]�������Ƃ��߂ɂ���";
	},	0,	"$cs{name}[$c]�ɐ����������"],
	[17,	'��׳����',				sub{
		$v = shift;
		# �������̔�J�� or �������ԒZ�k or �z���l+300
		# ����ݸ�����Ƃ��΋������������ł��I �z���l���������ł��I ����+6���ԃf�����b�g�̑ł�����
		# �����ł���Ίe�����m���Ō��ʔ����Ƃ��񕜒l�E�Z�k�l��{���ɔC����Ƃ��A�n�Y���v�f�Ƃ����ΑK���ԒZ�k���ǉ�����Ƃ��������z���l+100�Ƃ��i�z���l����f�����b�g�̖��ߍ��킹�j
		# ���ʂ̓A�������ǋ����f�����b�g�̑ł������������ƑI������������͂�z���l-100�̃f�����b�g�ł��������܂�2/3�Ńf�����b�g�ł������݂����Ȃ̂��ʔ�������
		# �������񐔂ɑ΂��Ĕ�J�񕜏o�����Ă���܂���������������Ȃ� ��J���炵�ěz���l�ǉ� �������������Ⴄ�O�ɉ��x��������������Ńv���C���[���Ɏ|�����Ⴄ �z���l�͍����ꗥ
		my $f = int(rand(3)); # 0 = ��J(1/3), 1 = ����(1/3), 2 = �z���l(1/3)
		my %sames;
		open my $fh, "< $logdir/$m{country}/member.cgi";
		while (my $player = <$fh>) {
			$player =~ tr/\x0D\x0A//d;
			# �������O�̐l����������ꍇ
			next if ++$sames{$player} > 1;
			if ($f == 0) { # ��J��
				&regist_you_data($player,'act', 0);
			}
			elsif ($f == 1) { # ��������ؾ��
				&regist_you_data($player,'next_salary', $time);
			}
			elsif ($f == 2) { # +500���z���l+300
				my %p = get_you_datas($player);
				&regist_you_data($player, 'egg_c',$p{egg_c} + 300);
			}
		}
		close $fh;

		if ($f == 0) { # ��J��
			$m{act} = 0;
		}
		elsif ($f == 1) { # ��������ؾ��
			$m{next_salary} = $time;
		}
		elsif ($f == 2) { # �z���l+300
			$m{egg_c} += 300;
		}

		return "�H��b�݂�$cs{name}[$m{country}]�̍��������에������";
	},	0,	"$cs{name}[$c]�ɐ����������"],
);
#=================================================
# �o�^���b�Z�[�W
#=================================================
sub regist_mes {
	$force = shift;
	$tm = qq|�y�K�E�Z�z|;
	my $attack = &get_attack;
	my ($a_year, $a_trigger, $a_timing, $a_demerit, $a_max_count, $a_effect, $a_voice, $a_count, $a_last_attack) = split /<>/, $attack;
	my $is_count = &count_check($a_max_count, $a_count, $a_last_attack);
	$attack = &get_attack;# �H�H�H
	if ($attack eq '' || $force) {
		$tm .= qq|<form method="$method" action="$script">|;

		$tm .= qq|<select name="trigger" class="menu1">|;
		for my $i (0..$#triggers) {
			next if !$triggers[$i][4];
			$tm .= qq|<option value="$i">$triggers[$i][1]</option>|;
		}
		$tm .= qq|</select>|;
		
		$tm .= qq|<br><select name="timing" class="menu1">|;
		for my $i (0..$#timings) {
			next if !$timings[$i][4];
			$tm .= qq|<option value="$i">$timings[$i][1]</option>|;
		}
		$tm .= qq|</select>|;
		
		$tm .= qq|<br><select name="demerit" class="menu1">|;
		for my $i (0..$#demerits) {
			next if !$demerits[$i][4];
			$tm .= qq|<option value="$i">$demerits[$i][1]</option>|;
		}
		$tm .= qq|</select>|;
		
		$tm .= qq|<br><select name="max_count" class="menu1">|;
		for my $i (0..$#max_counts) {
			next if !$max_counts[$i][3];
			$tm .= qq|<option value="$i">$max_counts[$i][1]��</option>|;
		}
		$tm .= qq|</select>|;
		
		$tm .= qq|<br><select name="effect" class="menu1">|;
		for my $i (0..$#effects) {
			next if !$effects[$i][3];
			$tm .= qq|<option value="$i">$effects[$i][1]</option>|;
		}
		$tm .= qq|</select>|;
		
		$tm .= qq|<br><input type="text" name="voice" class="text_box_b"/>|;
		$tm .= qq|<br><br><input type="checkbox" name="random" value="1"/>�K��|;
		$tm .= qq|<input type="hidden" name="regist_attack"/>|;
		$tm .= qq|<input type="hidden" name="mode" value="regist_attack">|;
		$tm .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
		$tm .= qq|<input type="submit" value="�K�E�Z��ݒ肷��" class="button1"></form>|;

	} else {
		my ($year, $trigger, $timing, $demerit, $max_count, $effect, $voice, $random, $last_attack) = split /<>/, $attack;
		unless ($is_count) {
	#		my ($a_year, $a_trigger, $a_timing, $a_demerit, $a_max_count, $a_effect, $a_voice, $a_count, $a_last_attack) = split /<>/, $attack_set;
	
			unless ($is_mobile) {
				$tm .= qq|<table class="table1" cellpadding="3">|;
				$tm .= qq|<tr><th>�s��</th><td>$triggers[$trigger][1]</td></tr>|;
				$tm .= qq|<tr><th>����</th><td>$timings[$timing][1]</td></tr>|;
				$tm .= qq|<tr><th>�f�����b�g</th><td>$demerits[$demerit][1]</td></tr>|;
				$tm .= qq|<tr><th>��</th><td>$max_counts[$max_count][1]��</td></tr>|;
				$tm .= qq|<tr><th>����</th><td>$effects[$effect][1]</td></tr>|;
				$tm .= qq|<tr><th>���</th><td>�u$voice�v</td></tr>|;
				$tm .= qq|</table>|;
			}
			else {
				$tm .= qq|<br>$triggers[$trigger][1]|;
				$tm .= qq|<br>$timings[$timing][1]|;
				$tm .= qq|<br>$demerits[$demerit][1]|;
				$tm .= qq|<br>$max_counts[$max_count][1]��|;
				$tm .= qq|<br>$effects[$effect][1]|;
				$tm .= qq|<br>�Z���t�u$voice�v|;
			}

#			$tm .= qq|<br>���̕K�E�Z�����܂� <font color="#FF0000"><b>�n�j�I</b></font>|;

			$tm .= qq|<br><form method="$method" action="$script">|;
			$tm .= qq|<input type="hidden" name="mode" value="use_attack">|;
			$tm .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
			$tm .= qq|<input type="checkbox" name="luxury" value="1">��ł�|;
			$tm .= qq|<input type="submit" value="�K�E�Z���g�p����" class="button1"></form>|;

			my $power_v = $triggers[$trigger][3] * $timings[$timing][3] * $demerits[$demerit][3] * $max_counts[$max_count][2] * (10 + ($cs{capacity}[$m{country}] - $cs{member}[$m{country}]) * 0.1);
			$tm .= qq|�\\�z�{�� <font color="#FF0000"><b>$power_v</b></font>|;
		}
		else {
			my $nokori_time = ($last_attack + $cooldown_time) - $time;
			my $nokori_time_mes = '';
			$nokori_time_mes = sprintf("��<b>%d</b>��<b>%02d</b>����", $nokori_time / 3600, $nokori_time % 3600 / 60);
			$tm .= qq|<br>�K�E�Z�̍Đݒ�܂� $nokori_time_mes|;
		}
	}

	return $tm;
}
#=================================================
# �K�E�Z�o�^
#=================================================
sub regist_attack {
	my ($trigger, $timing, $demerit, $max_count, $effect, $voice, $random) = @_;
	my $attack = &get_attack;

	if ($attack ne '') {
		&del_attack;
		return 0;
	}
	if ($random) {
		my @triggers_s = ();
		for my $i (0..$#triggers) {
			if ($triggers[$i][4]) {
				push @triggers_s, $i;
			}
		}
		if (rand(5) < 1) {
			$trigger = int(rand(@triggers));
		} else {
			$trigger = $triggers_s[int(rand(@triggers_s))];
		}
		
		my @timings_s = ();
		for my $i (0..$#timings) {
			if ($timings[$i][4]) {
				push @timings_s, $i;
			}
		}
		if (rand(5) < 1) {
			$timing = int(rand(@timings));
		} else {
			$timing = $timings_s[int(rand(@timings_s))];
		}
		
		my @demerits_s = ();
		for my $i (0..$#demerits) {
			if ($demerits[$i][4]) {
				push @demerits_s, $i;
			}
		}
		if (rand(5) < 1) {
			$demerit = int(rand(@demerits));
		} else {
			$demerit = $demerits_s[int(rand(@demerits_s))];
		}
		
		my @max_counts_s = ();
		for my $i (0..$#max_counts) {
			if ($max_counts[$i][3]) {
				push @max_counts_s, $i;
			}
		}
		if (rand(10) < 1) {
			$max_count = int(rand(@max_counts));
		} else {
			$max_count = $max_counts_s[int(rand(@max_counts_s))];
		}
		
#		my @effects_s = ();
#		if (rand(3) < 1) {
#			for my $i (0..$#effects) {
#				if ($effects[$i][3]) {
#					push @effects_s, $i if int(rand(100)) < 70;
#				}
#				else {
#					push @effects_s, $i;
#				}
#			}
#			$effect = $effects_s[int(rand(@effects_s))];
			$effect = int(rand(@effects));
#		} else {
#			for my $i (0..$#effects) {
#				if ($effects[$i][3]) {
#					push @effects_s, $i;
#				}
#			}
#			$effect = $effects_s[int(rand(@effects_s))];
#		}
	} else {
		if (!$triggers[$trigger][4]) {
			return 0;
		}
		if (!$timings[$timing][4]) {
			return 0;
		}
		if (!$demerits[$demerit][4]) {
			return 0;
		}
		if (!$max_counts[$max_count][3]) {
			return 0;
		}
		if (!$effects[$effect][3]) {
			return 0;
		}
	}
	open my $fh, ">> $this_file" or &error("$this_file�ɏ������߂܂���");
	if ($config_test) {
		print $fh "$w{year}<>$trigger<>$timing<>$demerit<>$max_count<>$effect<>$triggers[$trigger][1]�E$timings[$timing][1]�E$demerits[$demerit][1]�E$max_counts[$max_count][1]�E$effects[$effect][1]<>0<>$time<>\n";
	}
	else {
		print $fh "$w{year}<>$trigger<>$timing<>$demerit<>$max_count<>$effect<>$voice<>0<>$time<>\n";
	}
	close $fh;
	
	return 1;
}
#=================================================
# �K�E�Z�擾
#=================================================
sub get_attack {
	if (-f "$this_file") {
		open my $fh, "< $this_file" or &error("$this_file���ǂݍ��߂܂���");
		while (my $line = <$fh>) {
			my ($year, $trigger, $timing, $demerit, $max_count, $effect, $voice, $count, $last_attack) = split /<>/, $line;
			if ($year eq $w{year}) {
				close $fh;
				return $line;
			}
		}
		close $fh;
	}
	return '';
}
#=================================================
# �K�E�Z�폜
#=================================================
sub del_attack {
	if (-f "$this_file") {
		@lines = ();
		open my $fh, "+< $this_file" or &error("$this_file���ǂݍ��߂܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my ($year, $trigger, $timing, $demerit, $max_count, $effect, $voice, $count, $last_attack) = split /<>/, $line;
			if ($year eq $w{year}) {
				next;
			}
			push @lines, $line;
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
	}
}
#=================================================
# �K�E�Z����
#=================================================
sub cancel_attack {
	if (-f "$this_file") {
		@lines = ();
		open my $fh, "+< $this_file" or &error("$this_file���ǂݍ��߂܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my ($year, $trigger, $timing, $demerit, $max_count, $effect, $voice, $count, $last_attack) = split /<>/, $line;
			if ($year eq $w{year}) {
				$count++;
				push @lines, "$year<>$trigger<>$timing<>$demerit<>0<>$effect<>$voice<>$count<>$time<>\n";
			} else {
				push @lines, $line;
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
	}
}
#=================================================
# �K�E�Z�g�p
#=================================================
sub use_count_up {
	if (-f "$this_file") {
		@lines = ();
		open my $fh, "+< $this_file" or &error("$this_file���ǂݍ��߂܂���");
		eval { flock $fh, 2; };
		while (my $line = <$fh>) {
			my ($year, $trigger, $timing, $demerit, $max_count, $effect, $voice, $count, $last_attack) = split /<>/, $line;
			if ($year eq $w{year}) {
				$count++;
				push @lines, "$year<>$trigger<>$timing<>$demerit<>$max_count<>$effect<>$voice<>$count<>$time<>\n";
			} else {
				push @lines, $line;
			}
		}
		seek  $fh, 0, 0;
		truncate $fh, 0;
		print $fh @lines;
		close $fh;
	}
}
#=================================================
# �K�E�Z�񐔃`�F�b�N
#=================================================
sub count_check {
	my ($max_count, $count, $last_attack) = @_;
	if ($max_counts[$max_count][1] > $count) {
		return 0;
	} elsif ($last_attack + $cooldown_time < $time) {
		&del_attack;
		return 1;
	} else {
		return 1;
	}
}
#=================================================
# �K�E�Z����
#=================================================
sub super_attack {
	my $key = shift;
	unless ($m{country}) {
		return;
	}
	if ($time < $w{reset_time}) {
		return;
	}
	my $attack = &get_attack;
	if ($attack eq '') {
		return;
	}
	my ($year, $trigger, $timing, $demerit, $max_count, $effect, $voice, $count, $last_attack) = split /<>/, $attack;
	if ($key eq 'luxury') {
		&cancel_attack;
	}
	if ($key ne $triggers[$trigger][2] || rand(100) > $triggers[$trigger][5]) {
		return;
	}
#	$attackable = &{$timings[$timing][2]};
#	if (!$attackable) {
#		return;
#	}
	my $timing_v = &{$timings[$timing][2]};
	return unless $timing_v;
	if (&count_check($max_count, $count, $last_attack)) {
		return;
	}

	my $demerit_v = &{$demerits[$demerit][2]};
	return unless $demerit_v > 0;
#	return unless &{$demerits[$demerit][2]};
#	my $mem = &modified_member($m{country});
	$e_mes = $effects[$effect][2]->($triggers[$trigger][3]
#							* &{$timings[$timing][2]}
							* $timing_v
#							* $demerits[$demerit][3]
							* $demerit_v
							* $max_counts[$max_count][2]
#							* 11.2);
							* (10 + ($cs{capacity}[$m{country}] - $cs{member}[$m{country}]) * 0.1));
# �d����������Z�̋���ɗ^����e�����傫�� �l�����Ȃ��I�Ƒ����I�Ƃł��Ȃ�̍����o���ɏ��Ȃ��Ǝキ�����Ƌ����ŏI���ɂ��������I���̋ɒ[�Ȋ���
#							* (1 + ($cs{capacity}[$m{country}] - $mem) * 0.1)); # �d��������ɐV�K����񑽂��قǎ�̉��H ���Ԃ�t�ɂȂ��Ă�
#	$e_mes = $effects[$effect][4];
	&use_count_up;
	&mes_and_world_news("�K�E�Z���J�����A$e_mes�B<br><b>$m{name}�u$voice�v</b>", 1);
}

#=================================================
# �K�E�Z�̊�{���ʗʂ�n���ƕK�E�Z�̋������z��ŕԂ�($1, $2)
# $1�F���ٕ����i�ʏ�E���K�E�M�K�j
# $2�F���ʗʁi1�{�E1.2�{�E1.5�{�j��(1�{�E1.1�{�E1.3�{)
#=================================================
sub get_attack_level {
	my $attack_value = shift;
	my @level_names = ('', 'Ҷ�', '�޶�');
	my @level_values = (1, 1.1, 1.3);
	my $level = rand(100) < 10 ? 2 :
					rand(100) < 25 ? 1 :
					0;
	return ($level_names[$level], $attack_value*$level_values[$level]);
}

#=================================================
# �C���㏊���l��
#=================================================
sub modified_member {
	my $count_country = shift;
	my $count = 0;
	my @members = &get_country_members($count_country);
	for my $member (@members) {
		$member =~ tr/\x0D\x0A//d; # = chomp �]���ȉ��s�폜
		my $member_id = unpack 'H*', $member;
		my %datas = &get_you_datas($member_id, 1);
		unless ($datas{sedai} == 1) {
			$count++;
		}
	}
	return $count;
}

1;
#================================================
# upload picture
#================================================
sub begin {
	$mes .= "戻ります";
	$m{pet} = 168;
	&refresh;
	&n_menu;
}

sub tp_1  {
	$mes .= "戻ります";
	$m{pet} = 168;
	&refresh;
	&n_menu;
}

sub tp_100 {
	$m{tp} = 200;
	$mes .= '異次元の美術商<br>';
	$mes .= 'サイズ注意(15KBまで)<br>';
	&menu('やめる','異次元から絵を転送');
}

sub tp_200 {
	return if &is_ng_cmd(1);

	if ($cmd eq '1'){
	   $m{tp} = 300;
	   &{ 'tp_'. $m{tp} };
	}
	else
	{
		&refresh;
		&n_menu;
	}
}

sub tp_300 {
$layout = 2;
	$mes .= "<br>";
	$mes .= qq|<form action="upload.cgi" method="$method" enctype="multipart/form-data">|;
	$mes .= qq|<input type=file name="upfile">|;
	$mes .= qq|<input type=submit name=sub value="異世界から転送">|;
	$mes .= qq|<input type="hidden" name="id" value="$id"><input type="hidden" name="pass" value="$pass">|;
	$mes .= qq|</form>|;
	$m{tp} = 400;
}

sub tp_400 {
	&remove_pet if !-f "$userdir/$in{id}/upload_token.cgi";
	&refresh;
	&n_menu;
}

1;
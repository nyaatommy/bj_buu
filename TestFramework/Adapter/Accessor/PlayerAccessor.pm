####################################
# プレイヤーデータのアクセサ
# access_data以外の関数はプレイヤーの操作を疑似的に再現する
####################################

use warnings;
#use strict;

package PlayerAccessor;
require './TestFramework/Adapter/Accessor/Util.pm';
use CGI::Carp;

sub new{
	my $class = shift;
	my $self = {};

	return bless $self, $class;
}

#./user/user.cgiのデータを直接読み書きする
sub access_data{


	my $self = shift;
	my $user_name = shift;
	my $key = shift;
	
	croak ("user_name and key should be given\n") unless ((defined $user_name) and (defined $key)); 

	my $sub_routine = sub{

		_load_config();
		_read_user($user_name);

		#新しい値が設定されていれば設定、なければ取得
		if (@_){

			my $new_value = shift;
	
			#y_の形のkeyなら%yに設定
			if ($key =~ /^y_(.+)$/){
				$y{$1} = $new_value;
			}
			else{
				$m{$key} = $new_value;
			}
	
			&write_user;
			Util::_read_user($user_name);

		}

		if ($key =~ /^y_(.+)$/){
			return $y{$1};
		}
		else{
			return $m{$key};
		}
	};

	return Util::fork_sub($sub_routine);

}

#プレイヤーを作成する(new_entry.cgi経由)
sub create_player{

	my $self = shift;
	my ($name, $pass, $sex, $address) = @_;
	#new_entry.cgi経由で作成
	
	my $sub_routine = sub{

		_load_config();
		$ENV{REMOTE_ADDR} = $address;	
		$ENV{QUERY_STRING} = "mode=new_entry&name=$name&pass=$pass&sex=$sex";
		require 'new_entry.cgi';
	};

	return Util::fork_sub($sub_routine);



	
}

#プレイヤーを削除する(.lib/move_player.cgi経由)
sub remove_player{

	my $self = shift;
	my $name = shift;
	my $sub_routine = sub{

		_load_config();
		_read_user($name);

		require './lib/move_player.cgi';
		&read_cs;
		move_player($name, $m{country}, "del");
	};

	return Util::fork_sub($sub_routine);

}

#プレイヤーに士官させる(lib/system_game.cig::b_menu経由)
sub shikan_player{

	my $self = shift;
	my ($name, $to_country) = @_;

	my $sub_routine = sub{

		_load_config();
		_read_user($name);
		&read_cs;
		$mes = "";

		require "./lib/country_move.cgi";

		unless(&is_satisfy){
			return "is_satisfy() return 0\n";
		}
		$cmd = 1;
		$m{value} = $to_country;
		&tp_300;
		
		&write_user;

		return $mes;
	};

	return Util::fork_sub($sub_routine);

}

#playerにアイテムを与える
#todo
sub give_item{
}

#playerにアイテムを装備させる
#todo
sub set_item{
}

#playerに装備したペットを使用させる
#todo
sub use_item{
}
#プレイヤーを結婚登録所に登録させる
#todo
sub regist_marriage{
}	

#プレイヤーにプロポーズさせる
#todo
sub propose{
}

#プレイヤーにプロポーズを受けさせる
sub accept_propose{
#todo
}



#forkしたプロセスからbjのCGIをrequireする
sub _load_config{

	require "config.cgi";
	require "config_game.cgi";
}

#ユーザー名から%m,%yにデータ読み込み
sub _read_user{

	my $user_name = shift;

	my $id = unpack ('H*',$user_name);

	open my $fh, "< $userdir/$id/user.cgi" or croak("couldn't open ", $userdir, "/", $id, "/user.cgi");
	my $line = <$fh>;	
	close $fh;

	#pass検索
	my $pass;
	for my $hash (split /<>/, $line) {
		my($k, $v) = split /;/, $hash;
		if($k eq "pass") {
			$pass = $v;	
			last;
		}
	}

	#%m %yへユーザーデータ読み込み
	$in{id} = $id;
	$in{pass} = $pass; 
	&read_user;
}
1;

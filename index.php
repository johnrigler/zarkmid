<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
<meta http-equiv="content-type" content="text/html;charset=UTF-8">
<meta charset="utf-8">
<link rel="stylesheet" type="text/css" href="style.css">

</head>

<?php

function create_file($file_name) {

$file = fopen("./$file_name","w");
echo fwrite($file,"");
fclose($file);
chmod("./$file_name",0660);

};

if(isset($_POST['command']))
{
	list($first,$rest) = explode(" ",$_POST['command']);
	$next_move = "$first $rest";
	if($first == "save")
	{

		$next_move = "";
	}
}
else
	$next_move = "";



$file_name = "moves";
//$moveno = 0;

if (! file_exists($file_name))create_file($file_name);

if( 0 != filesize($file_name))
      {
      $file_moves = file($file_name);
      foreach ($file_moves as $moveno => $move)
        {
	list($first,$rest) = explode(" ",$move);
	$moves_str .= "$move";
      } 
}

      $moves_str .= "$next_move\n";
      $frotz = `echo "$moves_str" | dfrotz -s 1 /var/local/ZORKI.DAT`;

$old_moveno = $moveno;
$moveno = 0;
$target_stream = array();
$game_stream = explode("> ",$frotz);
foreach ($game_stream as $moveno => $desc)
{
	$desc_array = explode("\n",$desc);
	$target_stream[$moveno]['move'] = $file_moves[$moveno-1];
	$target_stream[$moveno]['status'] = array_shift($desc_array);
	array_shift($desc_array);
	$target_stream[$moveno]['desc'] = $desc_array;

}

if(isset($_POST['command']))
{
file_put_contents($file_name,$moves_str);
$target_stream[$moveno]['move'] = $next_move;
}

$target_elements = count($target_stream) - 1;
$last_target_desc_line = count($target_stream[$target_elements]['desc']);
unset($target_stream[$target_elements]['desc'][$last_target_desc_line - 3]);
unset($target_stream[$target_elements]['desc'][$last_target_desc_line - 1]);

//echo "<div>";
//print_r($target_stream[$target_elements]['desc']);
//echo "</div>";
//echo "$old_moveno $moveno";
// <table border=1>
// <tr><td width=700px>
// <img src=NFFFFFF-0.png width=1px height=1px>
?>
<pre>
<?php 

$status_array = explode(":", $target_stream[max(array_keys($target_stream))]['status']);
$game_location = trim(str_replace("Score","",$status_array[0]));
$game_score = trim(str_replace("Moves","",$status_array[1]));
$game_moves = trim($status_array[2]);
echo $target_stream[max(array_keys($target_stream))]['status']; 
?>
</pre>
<hr>
<div style="overflow-y: scroll; height=100px;">
<pre>
<?php
$display_arr = array();

foreach($target_stream as $move_item)
{
	$thismove = $move_item['move'];
	$display_arr []= "> $thismove\n";
	$thisdesc = $move_item['desc'];
	foreach($thisdesc as $line)
		$display_arr []= "$line\n";
}

$linecount = (int) count($display_arr);
if($linecount >= 36) 
	{
		$show = $linecount - 36;
		$takeback = 0;
}
else 
	{
		$show = -20;
		$takeback = 0;
}

foreach($display_arr as $count => $line)
{
	if($count > $show)
		if($count < $linecount - $takeback)
	                echo "$line";
}
?>
</div>
</pre>
Your Move:
<form method="post">
<input type=text name="command" maxlength="80" size="80" autocomplete="off" autofocus>
<?php
echo "<input type=hidden id='game_moves' name='game_moves' value=$game_moves >";
echo "</form>";
?>
</html>

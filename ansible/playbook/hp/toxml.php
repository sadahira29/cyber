<?php
$tokens = [
'hostname',
'dos-filter',
'no',
'cdp',
'run',
'enable',
'max-vlans',
'sntp',
'server',
'priority',
'time',
'timezone',
'ip',
'route',
'interface',
'name',
'exit',
'speed-duplex',
'snmp-server',
'community',
'operator',
'unrestricted',
'contact',
'location',
'vlan',
'untagged',
'address',
'tagged',
'management-vlan',
'spanning-tree',
'admin-edge-port',
'root-guard',
'bpdu-filter',
'bpdu-protection',
'tftp',
'fastboot',
'loop-protect',
'disable-timer',
'dhcp',
'config-file-update',
'image-file-update',
'password',
'manager',
'operator',
];

$cont = false;
$tag = '';

$fname = $argv[1];
if($fp = fopen($fname, "r")){
  echo('<?xml version="1.0" encoding="utf-8"?>'."\n");
  echo("<HP_config>\n");

  while($line = fgets($fp)){
    $line = chop($line);
    if($line != '' && $line[0] != ';'){
      toxml($line);
    }
  }
}
if($cont){
  echo("</".$tag.">\n");
}
echo("</HP_config>\n");

function toxml($line){
  global $tokens;
  global $cont;
  global $tag;

  if($line[0] != ' '){
    if($cont){
      echo("</".$tag.">\n");
    }
    $cont = true;
    $strs = str_getcsv($line, " ");
    foreach($strs as $str){
      if(in_array($str, $tokens, true)){
        if($str === reset($strs)){
	  $tag = $str;
          echo("<".$str.">\n");
        }else{
          echo("  <".$str."/>\n");
        }
      }else{
        echo("  <value>".$str."</value>\n");
      }
    }
  }else{
    $line = ltrim($line);
    $strs = str_getcsv($line, " ");
    if($strs[0] == 'exit'){
      $cont = false;
      echo("</".$tag.">\n");
    }else{
      foreach($strs as $str){
        if(in_array($str, $tokens, true)){
          if($str === reset($strs)){
	    if(count($strs) == 1){
              echo("  <".$str."/>\n");
	    }else{
              echo("  <".$str.">");
	    }
	  }else{
            echo("<".$str."/>");
	  }
        }else{
	  echo("<value>".$str."</value>");
        }
        if($str === end($strs)){
          echo("</".reset($strs).">\n");
	}
      }
    }
  }
}
?>
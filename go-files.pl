#!/usr/bin/perl -w
use strict;
use warnings;
use JSON;
$_ = join "", `go list -n -v -a -json -deps`;
# convert it to array of records before parsing
s/}\s*{/},{/g; 
my $json = JSON->new->utf8->decode("[$_]");
# now for each Dir list GoFiles
for my $m (grep $_->{Dir}, @$json) {
	my $d=$m->{Dir};
	$d =~ s{\\}{/}g; # windows understands "/" instead of "\\"
	print "$d/$_\n" for @{$m->{GoFiles}};
}
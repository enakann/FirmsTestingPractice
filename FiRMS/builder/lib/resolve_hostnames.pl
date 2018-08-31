#!/bin/perl
use Socket;
use Tie::File;

my $hostname;
my $ips_str;
my $host;
my $aliases;
my $name;
my $addrtype;
my $length;
my @addrs;

#filename as argument
my $filename = $ARGV[0];
tie my @data, 'Tie::File', $filename or die $!;
print "********************* \n";
print @data;
foreach my $indx(0..$#data){
    $addr = $data[$indx];
    $hostname = $addr;
    eval{
        if($addr =~ /(\d+\.)+(\d+)/){
            ($host, $aliases) = gethostbyaddr(inet_aton($addr), AF_INET);
            $hostname = $host;
        }
        unless($hostname){
            $data[$indx] = "$addr,";
        }
        else{
            ($name, $aliases, $addrtype, $length, @addrs) = gethostbyname($hostname);
            @ips = map{inet_ntoa($_)}@addrs;
            $ips_str = join(",",@ips);
            $data[$indx] = "$addr,$ips_str";
        }
    };
    if($@){
        $data[$indx] = "$addr,";
    }
}
print "********************* \n";
print @data;
my $outfile = $filename;
$outfile =~ s/_input/_output/g;
open FOUT, ">$outfile" or die "Cant open file $! \n";

foreach my $ip (@data) {
    print "$ip\n";
    print FOUT "$ip\n";
}

close FOUT;
print ($outfile);
#exit;
#untie @data;

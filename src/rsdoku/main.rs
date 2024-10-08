use std::env;
use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;


fn main() -> std::io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let mut reader: BufReader<File> = BufReader::new(File::open(&args[1])?);

    let mut linebuf = String::new();
    // let _ = reader.read_line(&mut linebuf);
    let x: &[_] = &['\r', '\n'];

    while reader.read_line(&mut linebuf).unwrap() > 0 {
        let _ = linebuf.trim_end_matches(x);
        let arr: [u8; 81] = linebuf
            .split("")
            .map(|chr| chr.parse::<u8>().unwrap())
            .collect::<Vec<u8>>()
            .try_into()
            .unwrap();

        // let mut arr: [u8; 81] = linebuf.split("").map(|x| x.parse::<u8>().unwrap()).try_into()?;
        println!("{:?}",arr

        );
        linebuf.clear();
        break;
    }

    // for line in reader.lines().map(|line| line.unwrap()) {
    //     println!("{:?}", line.split("").map(|x| x.parse::<u16>().unwrap()));
    //     let v: Vec<u16> = line.split("").map(|x| x.parse::<u16>().unwrap()).collect();
    // }


    Ok(())
}

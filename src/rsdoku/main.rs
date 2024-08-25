use std::env;
use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;




fn main() -> std::io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let reader: BufReader<File> = BufReader::new(File::open(&args[1])?);

    for line in reader.lines().map(|line| line.unwrap()) {
        println!("{:?}", line.split(""))
    }


    Ok(())
}

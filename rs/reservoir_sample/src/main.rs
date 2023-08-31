use rand::Rng;  
use std::fs::File;  
use std::io::{self, BufRead, BufReader, Write};  
use std::path::PathBuf;
use structopt::StructOpt;  
use indicatif::{ProgressBar, ProgressStyle}; 
  
#[derive(Debug, StructOpt)]  
#[structopt(name = "reservoir_sampling", about = "A simple implementation of reservoir sampling.")]  
struct Opt {  
    /// The input file path  
    #[structopt(short = "i", long = "input", parse(from_os_str))]  
    input: PathBuf,  
  
    /// The output file path  
    #[structopt(short = "o", long = "output", parse(from_os_str))]  
    output: Option<PathBuf>,  
  
    /// The sample size  
    #[structopt(short = "s", long = "sample")]  
    sample: usize,  
  
    /// Show progress  
    #[structopt(short = "v", long = "verbose")]  
    verbose: bool,  
}  

fn count_lines(path: &PathBuf) -> io::Result<usize> {  
    let file = File::open(path)?;  
    let reader = BufReader::new(file);  
    Ok(reader.lines().count())  
}  
  
fn main() -> io::Result<()> {  
    let opt = Opt::from_args();  
  
    let total_lines = count_lines(&opt.input)?;   

    let reader: Box<dyn BufRead> = Box::new(BufReader::new(File::open(&opt.input)?));
    let mut writer: Box<dyn Write> = match opt.output {  
        Some(path) => Box::new(File::create(path)?),  
        None => Box::new(io::stdout()),  
    };  
  
    let mut reservoir = vec![];  
    let mut rng = rand::thread_rng();  


    let pb = ProgressBar::new(total_lines as u64);
    pb.set_style(ProgressStyle::default_bar()
        .template("{spinner:.green} [{elapsed_precise}] [{bar:40.cyan/blue}] {pos}/{len} ({eta})")
        .progress_chars("#>-"));
  
    for (i, line) in reader.lines().enumerate() {  
        let line = line?;  
        if i < opt.sample {  
            reservoir.push(line);  
        } else {  
            let j = rng.gen_range(0..=i);  
            if j < opt.sample {  
                reservoir[j] = line;  
            }  
        }  
        if opt.verbose && i % 10_000 == 0{  
            pb.inc(10_000);
        }  
    }  
    pb.finish_with_message("done");
  
    for line in reservoir {  
        writeln!(writer, "{}", line)?;  
    }  
      
    Ok(())  
}  


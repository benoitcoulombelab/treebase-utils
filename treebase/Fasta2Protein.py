import logging
import re
import click


@click.command()
@click.option('--input', '-i', type=click.Path(exists=True), default='proteins.fa',
              help='Fasta file.')
@click.option('--output', '-o', type=click.Path(), default='proteins.txt',
              help='Proteins from Fasta file.')
def main(input, output):
    '''Copies proteins from FASTA file.'''
    logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    copy_proteins(input, output)

    
def copy_proteins(input, output):
    name_pattern = re.compile('^>(?:sp\|){,1}(?:tr\|){,1}(\w+)')
    with open(input, 'r') as infile, open(output, 'w') as outfile:
        for line in infile:
            if line.startswith('>'):
                match = name_pattern.match(line)
                if match:
                    protein = match.group(1)
                    outfile.write(protein)
                    outfile.write('\n')


if __name__ == '__main__':
    main()

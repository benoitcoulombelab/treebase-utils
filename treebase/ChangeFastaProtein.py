import logging
import re
import click


@click.command()
@click.option('--input', '-i', type=click.Path(exists=True), default='proteins.fa',
              help='Fasta file containing original names.')
@click.option('--names', '-n', type=click.Path(exists=True), default='proteins.txt',
              help='Tab separated file with original names in first column and new names in second.')
@click.option('--output', '-o', type=click.Path(), default='proteins-out.fa',
              help='Output.')
def main(input, names, output):
    '''Change protein names in FASTA file.'''
    logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    newnames = parsenames(names)
    changenames(input, newnames, output)

    
def parsenames(input):
    names = {}
    with open(input, 'r') as infile:
        for line in infile:
            if line.startswith('#'):
                continue
            columns = line.rstrip('\r\n').split('\t')
            if len(columns) < 2:
                logging.debug('Line {} does not have 2 columns'.format(line.rstrip('\r\n')))
            else:
                names[columns[0]] = columns[1]
    return names


def changenames(input, newnames, output):
    name_pattern = re.compile('^>(?:sp\|){,1}(?:tr\|){,1}(\w+)')
    with open(input, 'r') as infile, open(output, 'w') as outfile:
        for line in infile:
            if not line.startswith('>'):
                outfile.write(line)
                continue
            match = name_pattern.match(line)
            if not match:
                logging.warning('Line {} does not match pattern'.format(line))
                outfile.write(line)
                continue
            protein = match.group(1)
            if not newnames.get(protein):
                print (protein)
            newname = newnames.get(protein, protein)
            if newname:
                outfile.write(name_pattern.sub(newname, line))
            else:
                outfile.write(line)


if __name__ == '__main__':
    main()

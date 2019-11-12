import logging
import re
import click


@click.command()
@click.option('--input', '-i', type=click.Path(exists=True), default='organism.txt',
              help='Tab separated file with organism in one column.')
@click.option('--column', '-c', type=int, default=1,
              help='Column index where organisms are, starting at 0.')
@click.option('--output', '-o', type=click.Path(), default='organism-out.txt',
              help='Output.')
def main(input, column, output):
    '''Fix organism names.'''
    logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    fixorganism(input, column, output)

    
def fixorganism(input, index, output):
    removebrackets = re.compile('[\[\]]')
    removeparentheses = re.compile('\(.*\)')
    with open(input, 'r') as infile, open(output, 'w') as outfile:
        for line in infile:
            if line.startswith('#'):
                outfile.write(line)
                continue
            columns = line.rstrip('\r\n').split('\t')
            if len(columns) < index:
                logging.debug('Line {} does not have {} columns'.format(line.rstrip('\r\n'), index))
                outfile.write(line)
            else:
                columns[index] = removebrackets.sub('', columns[index])
                columns[index] = removeparentheses.sub('', columns[index])
                columns[index] = columns[index].strip()
                outfile.write('\t'.join(columns))
                outfile.write('\n')


if __name__ == '__main__':
    main()

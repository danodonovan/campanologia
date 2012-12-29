import logging

logger = logging.getLogger('django_debug')

printBells = ['%d' % i for i in range(1, 17)]
evenBells = ['2', '4', '6', '8', '0', 'T', 'B', 'D']
placeBells = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'E', 'T', 'A', 'B', 'C', 'D']

class Course(object):
    """
    Internal class for ringing the method - Example place notation
        VM Plain Bob Doubles  : "5","Plain Bob Doubles","5.1.5.1.5LH2","p"
        Hand written example  :  5x1x5x1x5 le 2
        Must be able to handle either, or combination!!
    """

    def __init__(self, nBells, notation, name):

        self.nBells = nBells
        self.bells = printBells[:nBells]
        self.rawNotation = notation
        (self.notation, self.leadHead) = self.sanitiseNotation( notation )
        logger.debug('%s sanitised place: %s lh %s' % (name, self.notation, self.leadHead))
        self.name = name

        self.allChanges = []

    def sanitiseNotation( self, n ):

        if n.find('LH') > 0:
            (nr, lh) = n.split('LH')
        else: # to cope with asymetric methods
            (nr, lh) = (n, None)

        i = 0
        (n_t, n) = ([], [])
        n_t_reset = False

        # there are edge case problems for Orignal N and Cheeky Little Place Minimus
        if len(nr) == 1:
            logger.debug('NOTICE SPECIAL CASE (notation len == 1)')
            # if we're dealing with original
            if nr[0] == '-':
                n.append('X')
                n.append('1')
                return (n, lh)
                # if we're dealing with original odd
            if nr[0] in ['3', '5', '7', '9', 'E', 'A', 'C']:
                n.append('X')
                n.append('1')
                return (n, lh)
            # if we're dealing with Cheeky Little Place
            elif nr[0] == '1':
                n.append('14')
                n.append('12')
                return (n, lh)

        while i < len( nr ):

            if n_t_reset:
                n_t = []

            if nr[i] == '-':
                if n_t:
                    n.append( ''.join(n_t) )
                    n_t = []
                n.append( 'X' )
                n_t_reset = True
            elif nr[i] in placeBells:
                n_t.append( nr[i] )
                n_t_reset = False
            else:
                n.append( ''.join(n_t) )
                n_t_reset = True

            i += 1

        if n_t != []:
            n.append( ''.join(n_t) )

        return (n, lh)

    def _change(self, p=None):

        b = self.bells

        # If naughty people include ambiguous changes
        if p[0] in placeBells:
            if p[0] in evenBells:
                p = '1'+p

        i = 0
        while i < len(b)-1:
            if (placeBells[i] in p) or (placeBells[i+1] in p):
                i += 1
            else:
                b[i], b[i+1] = b[i+1], b[i]
                i += 2

    def ring(self):

        self.allChanges, self.leadends = [], []

        # NB - lh sometimes none to cope with asymetric methods
        (n, lh) = (self.notation, self.leadHead)

        nn = len( n )

        rung      = set()
        rounds    = self.bells[:]
        changes   = [tuple(rounds)]
        b         = self.bells

        (l_i, p_i, leadEnd_i, reverse, leadEnd) = (0, 0, 0, False, False)

        logger.debug('%s % 3d, % 3s, % 5s,  % 5s %s' % (self.name, 1, 'Go!', False, False, self.printChange(bells_print=rounds)))
        logger.debug('%s % 3d, % 3s, % 5s,  % 5s %s' % (self.name, 1,   '-', False, False, self.printChange(bells_print=rounds)))

        # Keep ringing until it comes round
        while b != rounds or l_i == 0:

            # for methods where places are not reversed (half lenght)
            if not lh and not p_i:
                self.leadends.append(b[:])
                leadEnd_i += 1

            if not leadEnd or not lh:
                self._change(p=n[p_i])
            else:
                leadEnd_i += 1
                self.leadends.append(b[:])
                self._change(p=leadEnd)

            logger.debug('%s % 3d, % 3s, % 5s,  % 5s %s' % (self.name, p_i, n[p_i], reverse, leadEnd, self.printChange(bells_print=['1', '2'])))

            self.allChanges.append(b[:])

            # Must write this logic out at some point
            if leadEnd:
                leadEnd = False
                p_i     = 0
                continue

            ## if in first half, increase place notation counter - else decrease counter
            if lh:
                if not reverse: p_i += 1
                else:           p_i -= 1
            else:
                if p_i == nn - 1:
                    p_i = 0
                else:
                    p_i += 1

            ## Mark the half lead and lead end
            if p_i == nn - 1: reverse = True
            if p_i < 0:       reverse = False

            ## test to see if we are at a lead end
            if (p_i == -1):
                leadEnd = lh
            else:
                leadEnd = False

            ## Just count the changes
            l_i += 1

            # keep track of what's been rung - spot falseness
            # if tuple(b) in rung:
            if b in changes:
                print '&&& False method &&& : %d' % changes.index(b)
                return

            rung.add(tuple(b))
            changes.append(tuple(b))
            # changes.append( b )

        # return tuple( changes )
        self.nleadends = leadEnd_i
        return changes

    def printChange(self, bells_print=['1']):
        b = self.bells
        print_string = ''
        for i in range(self.nBells):
            if b[i] in bells_print:
                print_string += '%2s ' % b[i]
            else:
                print_string += '%2s ' % ' '
        return print_string


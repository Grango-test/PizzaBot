from transitions import Machine


class PizzaBot(object):

    # Possible states
    states = ['asleep', 'size_order', 'payment_method', 'confirmation', 'cancel', 'confirm']

    def __init__(self):

        self.machine = Machine(model=self, states=PizzaBot.states, initial='asleep')

        self.machine.add_transition(trigger='start', source='asleep', dest='size_order')
        self.machine.add_transition(trigger='next', source='size_order', dest='payment_method')
        self.machine.add_transition(trigger='next', source='payment_method', dest='confirmation')
        self.machine.add_transition(trigger='confirm', source='confirmation', dest='confirm')
        self.machine.add_transition(trigger='cancel', source='size_order', dest='cancel')
        self.machine.add_transition(trigger='cancel', source='payment_method', dest='cancel')
        self.machine.add_transition(trigger='cancel', source='confirmation', dest='cancel')
        self.machine.add_transition(trigger='end', source='cancel', dest='asleep')
        self.machine.add_transition(trigger='end', source='confirm', dest='asleep')

        self.size = None
        self.payment_method = None

    def set_size(self, size):
        self.size = size

    def set_payment_method(self, payment_method):
        self.payment_method = payment_method
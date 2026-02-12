num_of_steps = 3
has_header = True
file_name = "result"
extension = "txt"
path = "data.csv"
text_template = """We made {lines} observations by tossing a coin: {tails} were tails and {heads} were heads. The probabilities are {right:.2f}% and {left:.2f}%, respectively. Our forecast is that the next {num} observations will be: {tails_predict} tail and {heads_predict} heads."""

from analytics import *
from config import *
import os

if __name__ == "__main__":
    if os.path.isfile(path):
        research = Research(path)
        research.file_reader(has_header)

        predict = research.Analytics(research.data)
        heads_n_tails = predict.counts()
        percents = predict.fractions(predict.heads, predict.tails)
        rolls = predict.predict_random(num_of_steps)

        rolling = research.Calculations(rolls)
        new_hd_n_ts = rolling.counts()

        result = text_template.format(
            lines=len(research.data),
            heads=heads_n_tails[0],
            tails=heads_n_tails[1],
            left=percents[0],
            right=percents[1],
            num=num_of_steps,
            heads_predict=new_hd_n_ts[0],
            tails_predict=new_hd_n_ts[1],
        )
        print(result)
        predict.save_file(result, file_name, extension)
    else:
        raise Exception("invalid file")

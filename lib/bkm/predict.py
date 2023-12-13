import argparse
import hydra

import pandas as pd

from lib.bkm.src import *
from omegaconf import DictConfig

# parser = argparse.ArgumentParser()
# parser.add_argument("--config-name", dest='config_name', default="exp_0", type=str)
# args = parser.parse_args()

def predict_wrapper(df:pd.DataFrame):
    result = []
    
    @hydra.main(version_base=None, config_path='E:/nlp_stock_recommand/lib/bkm/config', config_name="exp_0")
    def predict(cfg: DictConfig):
        from transformers import AutoTokenizer
        from torch.utils.data import DataLoader

        model = BertSum_Ext(**cfg.model)
        tokenizer = AutoTokenizer.from_pretrained(cfg.model.base_checkpoint)

        pred_df = prep_pred_df(df)
        pred_dataset = ExtSum_Dataset(pred_df, tokenizer, cfg.max_seq_len)
        pred_loader = DataLoader(pred_dataset, batch_size=1, shuffle=False)

        engine = ExtSum_Engine(model, test_df=pred_df, **cfg.engine)
        cfg_trainer = Config_Trainer(cfg.trainer)()
        trainer = pl.Trainer(**cfg_trainer, logger=False)

        if 'pred_checkpoint' in cfg:
            prediction = trainer.predict(engine, pred_loader, ckpt_path=cfg.pred_checkpoint)
        else:
            raise RuntimeError('no checkpoint is given')
        
        for pred in prediction:
            result.append(pred["prediction"][0])
            
    predict()
    return result

if __name__ == "__main__":
    predict()

import pandas as pd
import os
import time




class FNO:
    
    def __init__(self, *args, **kwargs):
        for k,v in kwargs.items():
            exec('self.%s = %s' %(k,v))

    def exec_all(self):
        self.read_files()
        self.get_rtns()
        self.get_lot_sizes()
        self.get_num_lots()

    def read_files(self):
        files = [os.path.join(self.fno_folder,f) for f in os.listdir(self.fno_folder)[:10]]
        self.fno_bhav_df = pd.DataFrame()
        for file in files:
            df = pd.read_csv(file)
            df = df[(df['INSTRUMENT'] == 'OPTSTK') & (df['OPEN_INT'] > 0) & (df['OPEN_INT'] != 0.0)]
            self.fno_bhav_df = self.fno_bhav_df.append(df)
        self.fno_bhav_df.drop_duplicates(inplace=True)
        self.fno_bhav_df['Sym_Exp_Concat'] = self.fno_bhav_df['SYMBOL'].map(str) + self.fno_bhav_df['EXPIRY_DT'].map(str)
        # print(self.fno_bhav_df)

    def get_rtns(self):
        self.fno_bhav_df['Concat'] = self.fno_bhav_df['SYMBOL'].map(str) + self.fno_bhav_df['EXPIRY_DT'].map(str) + self.fno_bhav_df['STRIKE_PR'].map(str) + self.fno_bhav_df['OPTION_TYP'].map(str)
        self.closing_price_df = pd.pivot_table(self.fno_bhav_df, values='CLOSE', index=['Concat','TIMESTAMP']).reset_index()
        self.closing_price_df['NEXT_CLOSE'] = self.closing_price_df['CLOSE'].shift(-1)
        # self.closing_price_df.dropna(subset=['NEXT_CLOSE'], inplace=True)
        # self.closing_price_df['Price Change'] = self.closing_price_df['CLOSE'] - self.closing_price_df['NEXT_CLOSE']
        print(self.closing_price_df)
        self.closing_price_df.to_csv(r'closing.csv')
        
    def get_lot_sizes(self):
        self.pvt = pd.pivot_table(self.fno_bhav_df, index=['SYMBOL','EXPIRY_DT'], aggfunc='min', values=["OPEN_INT"]).reset_index()
        self.pvt.rename(columns={'OPEN_INT':'LOT_SIZE'}, inplace=True)
        self.pvt['Sym_Exp_Concat'] = self.pvt['SYMBOL'].map(str) + self.pvt['EXPIRY_DT'].map(str)
        # self.pvt.to_csv(r'lot_sizes.csv')

    def get_num_lots(self):
        self.final_df = self.fno_bhav_df.merge(self.pvt[['Sym_Exp_Concat','LOT_SIZE' ]], how='left', on=['Sym_Exp_Concat'])
        print(self.final_df)
        self.final_df['Num_Lots'] = self.final_df['OPEN_INT']/self.final_df['LOT_SIZE']
        self.final_df = self.final_df[self.final_df['Num_Lots'] >= self.min_lots]
        self.final_df['Concat'] = self.final_df['SYMBOL'].map(str) + self.final_df['EXPIRY_DT'].map(str) + self.final_df['STRIKE_PR'].map(str) + self.final_df['OPTION_TYP'].map(str)
        self.final_df = self.final_df.merge(self.closing_price_df[['Concat','NEXT_CLOSE']], how='left', on='Concat')
        print(self.final_df)
        self.final_df.to_csv(r'output.csv', index=False)


if __name__ == '__main__':
    start = time.time()
    fno_folder = r'D:\OneDrive\Trading\High OI\FnO Bhavcopy'
    min_lots = 3000
    fno = FNO(fno_folder="r'%s'"%fno_folder, min_lots=min_lots)
    fno.exec_all()
    end = time.time()
    tot_time = (end - start)/60
    print('Time taken : %d' %tot_time)

import pandas as pd
import requests
from pandas import DataFrame
from tqdm.notebook import tqdm

class OnlineTableRetriever:
    def get_table_from_url(
        self,
        url: str
    ) -> DataFrame:
        header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
        }

        r = requests.get(url, headers=header)
        df = pd.read_html(r.text)
        assert len(df) == 1, 'More than one table present in the page'

        return df[0]

    def _treat_currency_columns(
        self,
        df, 
        currency='R$'
    ) -> DataFrame:
        currency = f'{currency.strip()} '
        for name, _ in df.iteritems():
            if df[name].dtype == object: 
                df[name] = df[name].str.replace(currency, '', regex=False)
        return df

    def _treat_percentage_columns(
        self,
        df
    ) -> DataFrame:
        for name, _ in df.iteritems():
            if df[name].dtype == object and df[name].str.endswith('%').any():
                df[name] = df[name].str.replace('%', '', regex=False)
        return df

    def _treat_numeric_columns(
        self,
        df
    ) -> DataFrame:
        for name, _ in df.iteritems():
            if df[name].dtype == object:
                if df[name].isna().any():
                    df[name] = df[name].fillna(0.0)
                df[name] = df[name].str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
                if df[name].str.isdecimal().all():
                    df[name] = df[name].astype(int)
                elif df[name].str.contains('.', regex=False).any():
                    df[name] = df[name].astype(float)
        return df

    def get_foundsexplorer_data(
        self
    ) -> DataFrame:
        url = "https://www.fundsexplorer.com.br/ranking"
        df = self.get_table_from_url(url)

        df.loc[:, ['Liquidez Diária']] = self._treat_numeric_columns(df.loc[:, ['Liquidez Diária']])
        df = self._treat_currency_columns(df)
        df = self._treat_percentage_columns(df)
        df = self._treat_numeric_columns(df)
        df.fillna(0.0, inplace=True)
        df['P/VPA'] /= 100

        df.rename(columns={'Códigodo fundo': 'Papel'}, inplace=True)

        return df.sort_values(by='Papel').reset_index(drop=True)

    def get_fundamentus_data(
        self,
        real_state: bool = False,
        filtro_liquidez: int = 0
    ) -> DataFrame:
        fii = 'fii_' if real_state else ''
        url = f'https://www.fundamentus.com.br/{fii}resultado.php'
        df = self.get_table_from_url(url)

        df = self._treat_percentage_columns(df)
        df = self._treat_numeric_columns(df)

        df['P/VP'] /= 100
        df['Cotação'] /= 100
        if not real_state:
            df['P/L'] /= 100
            df['PSR'] /= 1000
            df['P/Ativo'] /= 1000
            df['P/Cap.Giro'] /= 100
            df['P/EBIT'] /= 100
            df['P/Ativ Circ.Liq'] /= 100
            df['EV/EBIT'] /= 100
            df['EV/EBITDA'] /= 100
            df['Liq. Corr.'] /= 100
            df['Dív.Brut/ Patrim.'] /= 100
            df = df[df['Liq.2meses'] > filtro_liquidez]
        else:
            df = df[df['Liquidez'] > filtro_liquidez]


        return df.sort_values(by='Papel').reset_index(drop=True)

    def get_fundamentus_sectors(
        self,
        fundaments_df: DataFrame
    ) -> DataFrame:
        header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
        }

        tickers = fundaments_df['Papel']
        sectors = list()

        df = fundaments_df.copy()

        for ticker in tqdm(tickers):
            r = requests.get(f'https://www.fundamentus.com.br/detalhes.php?papel={ticker}', headers=header)
            sector = pd.read_html(r.text)[0].iloc[3, 1]
            sectors.append(sector)
        df['Setor'] = sectors
        return df

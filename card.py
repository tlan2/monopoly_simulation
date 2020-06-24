# Card Class

class Card:
    """ Creates individual Chance & Community Chest cards  """
    
    def __init__(self, df, i):
        self.id = int(df.loc[i,'id'])
        self.category = df.loc[i,'category']
        self.action = (df.loc[i,'action'])
        self.text = df.loc[i,'text']
  
conf = {
    'ocean'   : {'ocean'  :2, 'shore'   :1},
    'shore'   : {'ocean'  :1, 'shore'   :0.5,'plains'  :10},
    'plains'  : {'shore'  :1, 'plains'  :1,  'forrest' :1,   'mountain':1},
    'forrest' : {'plains' :1, 'forrest' :5,  'mountain':0.5, 'ruin'    :0.1},
    'mountain': {'plains' :5, 'mountain':1,  'forrest' :0},
    'ruin'    : {'forrest':1},
}

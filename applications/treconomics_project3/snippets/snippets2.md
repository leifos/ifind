## query: wildlife
## tf-idf: 
## doc: 
[In Kenya'S Farmers Vs. Wildlife, The Animals Are Losing](https://gist.github.com/mickeypash/349e4a21511379ae9ea9)

# Whoosh snippet

```
show, Kenya's <b>wildlife</b>
has been disappearing...of the Kenya <b>Wildlife</b>
Service, David...former head of the <b>wildlife</b> service, Richard
```

# PyTease snippets

1.
```
These farmers
have plowed under and overgrazed buffer zones around parks and
reserves that the animals must use as dispersal areas during wet
seasons, wildlife officials say.
This is a semi-arid area.''
```

2.
```
Even some of the older farmers in Mramba support the idea.
Under current Kenyan law, the state owns all
wildlife, and it is illegal to sell or hunt them without a permit.
Farmers there report constant problems, mostly
lions killing cattle and elephants eating crops.
He and other conservationists
maintain it is a pipe dream to think such schemes can reverse the
underlying causes of the decline.
```

# Named Entity extraction

```
'East Africa Wildlife Society', 'Kenya', 'Hilton Hotels', 'Patitas', 'Crisant Mueme', 'Kenya Wildlife Service', 'Mwamburi Mwikamba', 'David Western', 'Kenyan', 'James Ndungu', 'KITENGELA', 'Mramba Group Ranch', 'Patita', 'Tsavo', 'Rob Barnett', 'Nairobi National Park', 'Traffic', 'Western', 'Samburu', 'Nehemiah Rotich', 'Richard Leakey', 'Kitengela', 'Jacob Nzalu', 'Taita', 'African', 'Wild', 'Nicholas Georgiadis', 'Mueme', 'Mpala Research Center', 'Mwikamba', 'Laikipia', 'Mwambili', 'Voi', 'Thomson', 'Taita Hills', 'Mramba', 'Richard Mwambili', 'Mohammed Dhidha', 'Leakey', 'Agnes Patita', 'Hirola'

```

# Summy 

1. LSASummarisation
```
</p><p> While the government's anti-poaching efforts, begun in the late 1980s, dramatically slowed down the wholesale slaughter of elephants and rhinoceroses in the last eight years, the local police have done little or nothing to stop a burgeoning underground trade in bush meat, conservationists say.
</p><p> Competition for land over the last 25 years has forced tens of thousands of Taita people, who in the past lived on the fertile slopes of the mountains, to move down onto the rangelands below, an arid savannah that was carved up into large communal ranches for cattle grazing in the 1960s.
```
2. LexRankSummariser
```
<p> KITENGELA, Kenya _ On a clear day, Agnes Patita can see the tourists in vans inching along dirt roads, searching the plains for antelope, zebra, giraffe and, if they are lucky, an elusive pride of lions.
</p><p> But the majestic cats the tourists pay to see are dangerous pests to Mrs. Patita.
```

3. LuhnSummariser
```
<p> KITENGELA, Kenya _ On a clear day, Agnes Patita can see the tourists in vans inching along dirt roads, searching the plains for antelope, zebra, giraffe and, if they are lucky, an elusive pride of lions.
</p><p> But the majestic cats the tourists pay to see are dangerous pests to Mrs. Patita.
(treconomics3-dev)leifs-MacBook-Pro:snippets mickeypash$ python summarization2.py 
</p><p> One camp, led by the current director of the Kenya Wildlife Service, David Western, wants to find ways to make wildlife profitable for local people and give them a reason to protect the animals.
</p><p> Another, led by the former head of the wildlife service, Richard Leakey, argues that Kenya should instead fence off wild lands, more strictly enforce anti-poaching laws and, in essence, give up on trying to stop the decline of wildlife elsewhere.
```
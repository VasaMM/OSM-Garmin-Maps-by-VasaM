all: ol cz sk ua ro kg


# Olomouc
ol: OL
OL:
	./makeMap.sh -a OL -ns


# Cesko
cz: CZ
CZ:
	./makeMap.sh -a CZ -dy


# Slovensko
sk: SK
SK:
	./makeMap.sh -a SK -dy


# Ukrajina
ua: UA
UA:
	./makeMap.sh -a UA -dy


# Rumunsko
ro: RO
RO:
	./makeMap.sh -a RO -dy


# Kyrgyzstan
kg: KG
KG:
	./makeMap.sh -a KG -dy


# Kazachstan
kz: KZ
KZ:
	./makeMap.sh -a KZ -dy

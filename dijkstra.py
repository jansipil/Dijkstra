def luetiedosto():

	"""
	Funktio kysyy käyttäjältä tiedoston nimeä, kunnes annetaan kelpaava tiedosto 
	return = tiedostosta luettu lista jossa on kaikki kaupungit ja ja niiden väliset kuormarajat
	"""


	lista = []

	while True:

		tiedosto = input("Anna tiedoston nimi: ")

		try:
			with open(tiedosto, "r") as kohde:
				for rivi in kohde:
					lista.append((rivi.rstrip()).split())

				return lista
				
		except IOError:
			print("Kohdetiedostoa ei voitu avata. Yritä uudelleen")


def algoritmi(verkko, alku, loppu, menneet=[], matkat={}, edelliset={}):
	"""
	rekursiivinen algoritmi funktio laskee verkolle djikstran algoritmia käyttäen parhaan mahdollisen reitin


	param verkko = sanakirja josta kaikki kaupunkien väliset yhteydet löytyvät
	param alku = kohta mistä funktio alkaa tutkimaan viereisiä kaupunkeja, alussa '1', myöhemmin se kaupunki missä ollaan menossa
	param loppu = päätepiste eli viimeinen kaupunki
	param menneet = lista, josta nähdään mitkä kaupungit on käyty jo läpi kokonaan, joten niitä ei aleta enää käsittelemään uudelleen.
	param matkat = sanakirja, jossa säilytetään sillä hetkellä suurinta sallittua kuormaa. sanakirja sen takia että voidaan käyttää sanakirjojen get() funktiota
	param edelliset = sanakirja jonka avulla saadaan kuljettu polku kaupunkien välillä. sanakirjaan lisätään arvo aina kun siirrytään seuraavaan kaupunkiin
	"""

	polku = [] # lista johon lopullinen kuljettu polku tallennetaan
	jaljella = {} # sanakirja niistä kaupungeista verkossa mitä ei ole vielä käsitelty

	if alku == loppu: # testataan ollaanko viimeisessä kaupungissa
		edellinen = loppu
		while edellinen != None: # lähdetään kulkemaan menty reitti takaperin kunnes päästään alkuun
			polku.append(edellinen)
			edellinen = edelliset.get(edellinen, None)
		kuorma = matkat[loppu] - 8 # lopullinen sallittu kuorma
		if kuorma < 8: # todetaan vielä että jos painoraja alle 8 niin ei pystytä kulkemaan auton painon takia
			print("Ei reittiä")
		else: # muutoin käännetään polku oikein päin ja tulostetaan se sekä kuormaraja
			polku.reverse()
			print("reitti: " + "->".join(polku) + " kuorma: " + str(kuorma))

	else:
		if not menneet: # ensimmäisellä kerralla mentäessä funktioon ei ole vielä mitään siltoja joten kuorma voi olla loputon
			matkat[alku] = float('inf')
		for reitti in verkko[alku]: # käydään läpi kaikki kyseisen kaupungin naapurit
			if reitti not in menneet: # jos ne eivät ole jo käyty läpi kerran
				maxkuorma = min(matkat[alku], verkko[alku][reitti]) 
				# maxkuorma on aina pienempi kahdesta: edellinen silta vai nyt tarkistettava silta, sillä kuorma ei voi enää nousta sen jälkeen kun sillasta on kuljettu
				if maxkuorma > matkat.get(reitti, 0): # käydään siltoja läpi ja valitaan se jolla on isoin painoraja
					matkat[reitti] = maxkuorma
					edelliset[reitti] = alku

		menneet.append(alku) # lisätään käsitelty kaupunki menneisiin
		for i in verkko: # muodostetaan jäljellä olevat käsiteltävät kaupungit
			if i not in menneet:
				jaljella[i] = matkat.get(i, 0)
		try: # käytettään max() funktiota iteroimaan sankirja läpi ja poimimaan suurin arvo seuraavaksi käsittelyyn
			seuraava = str(max(jaljella, key=jaljella.get)) 
		except ValueError: # jos sanakirja on tyhjä niin tiedetään että kaupunkeja ei enää ole
			seuraava = loppu
		#print(jaljella)
		#print(seuraava)
		#print("\n")
	
		algoritmi(verkko, seuraava, loppu, menneet, matkat, edelliset) # funktio kutsuu nyt itseään seuraavan kaupungin arvolla 




def main():

	verkko = {} # matriisi toteutettuna sanakirjaan, tulee sisältämään kaikki kaupnkien yhteydet
	# esim. verkon kohdassa "1:" sijaitsee kaikki kaupunki 1:sen reitit toisiin kaupunkeihin ja niiden kuormarajat

	lista = luetiedosto()
	
	alku = '1' # aloitetaan ilmeisesti aina kaupungista '1'
	loppu = lista.pop() # otetaan pois listan viimeinen luku ja saadaan siitä päätepiste
	lista.pop(0) # otetaan pois listan ensimmäisenä olevat arvot sillä niitä ei tarvita

	# looppi lisää nyt verkkoon listasta löytyvät reitit
	# looppi lisää kaupungeille kaikki niiden väliset reitit eli myös ne mitä tiedostossa ei toisteta, jos ne on kerran jo mainittu aiemmin kaupunkien välille
	for kohde in lista:
		if kohde[0] in verkko:
			verkko[kohde[0]][kohde[1]] = int(kohde[2])
			if kohde[1] in verkko:
				verkko[kohde[1]][kohde[0]] = int(kohde[2])
			else:
				verkko[kohde[1]] = {kohde[0]: int(kohde[2])} # jos kohdetta ei vielä ollut verkossa niin luodaan se
		else:
			verkko[kohde[0]] = {kohde[1]: int(kohde[2])}
			verkko[kohde[1]] = {kohde[0]: int(kohde[2])}
		
	#print(verkko)
	algoritmi(verkko, alku, loppu[0])





if __name__ == "__main__":
	main()
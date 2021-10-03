"""El famoso Bot Loup Garou"""

import asyncio
import time
from random import choice, shuffle

import discord
from discord.ext import commands

##from roles import *


TOKEN = 'NzY1MjQxMTcwNTAxOTU5Njgw.X4R8YA.FT6fPztuIWWJIUn3fB7NwNB0oD8'

CLIENT = discord.Client()
CLE = '!'

EMO_ID = {'chloe' :     (696410379961761853, '<:rosa:696469458868502539>',                 'Chloé'),
          'gautier' :   (696364394086662235, '<:gautier_n1:695748371696320553>',         'Gautier'),
          'guillaume' : (690210437878644915, '<:new_porK:776232685525008405>',         'Guillaume'),
          'tristan' :   (239676480697794560, '<:tristan_defonce:696489144305844246>',    'Tristan'),
          'theo' :      (616340560172548267, '<:theo:695760646871973958>',                  'Théo'),
          'louis' :     (395234795413700619, '<:louis4:696485582741962865>',               'Louis'),
          'iyad' :      (688805292775178375, '<:iyad_millionaire:696432299377557544>',      'Iyad'),
          'lucas' :     (488241503701958656, '<:lucas:778969059541647410>',                'Lucas'),
          'matheo' :    (605133570171994145, '<:ravioli:722123301471780995>',             'Mathéo')}

# Roles disponibles :
# villageois, loup, sorcière, garde, voyante, chaceur, cocktailiste
# Des configs de base à n joueurs
CONFIGS_6 = [['loup', 'loup', 'villageois', 'villageois', 'villageois', 'villageois']]
CONFIGS_7 = []
CONFIGS_8 = []
CONFIGS_9 = []

CONFIGS = [-1, -1, -1, -1, -1, -1, CONFIGS_6, CONFIGS_7, CONFIGS_8, CONFIGS_9]

# ______ NE RIEN MODIFIER EN DESSOUS DE CETTE LIGNE SANS AVOIR COMPRIS COMMENT CA MARCHE ___________
## Définition des rôles
class Voyante:
    """Le rôle de la voyante"""
    def __str__(self):
        return "Voyante"

    def __init__(self, joueur):
        self.soi = joueur
        self.couple = None

    async def informe(self):
        await envoi(EMO_ID[self.soi][0], "Tu seras une voyante pour cette partie")

    async def nuit(self, VIVANTS, PROTECT, VICTIME):
        txt = "De quelle personne souhaites-tu découvrir la véritable identité ?"
        sonde = await demande(EMO_ID[self.soi][0], txt, 15)
        if sonde != -1:
            txt = f'Le rôle de {EMO_ID[sonde][2]} est '
            txt += str([x for x in VIVANTS if x.nom_std == sonde][0].role)
            await envoi(EMO_ID[self.soi][0], txt)

    async def mort(self, VIVANTS):
        channel = CLIENT.get_channel(778578524193030184)
        await channel.send(f"{EMO_ID[self.soi][2]} était la voyante")

        if self.couple != None:
            self.couple.role.mort(VIVANTS)
            VIVANTS.remove(self.couple)

class Garde:
    """Le rôle du garde"""
    def __str__(self):
        return "Garde"

    def __init__(self, joueur):
        self.soi = joueur
        self.prec = None
        self.couple = None

    async def informe(self):
        await envoi(EMO_ID[self.soi][0], "Tu seras un garde pour cette partie")

    async def nuit(self, VIVANTS, PROTECT, VICTIME):
        txt = "Quelle personne souhaites-tu protéger des menaces de la nuit ?"
        if self.prec != None:
            txt_opt = f"\n({EMO_ID[self.prec][2]} a été protégé au tour précédent et "
            txt_opt = "ne peut donc l'être à nouveau cette nuit)"
            txt += txt_opt
        sonde = await demande(EMO_ID[self.soi][0], txt, 15)
        if sonde != -1 and sonde != self.prec:
            self.prec = sonde
            poss = [x for x in VIVANTS if x.nom_std == sonde]
            if len(poss) == 1:
                PROTECT.append(poss[0])
                txt = f'{EMO_ID[sonde][2]} sera protégé cette nuit'
        else:
            txt = "Ton choix n'est pas valide ou n'a pas été pris en compte..."
        await envoi(EMO_ID[self.soi][0], txt)

    async def mort(self, VIVANTS):
        channel = CLIENT.get_channel(778578524193030184)
        await channel.send(f"{EMO_ID[self.soi][2]} était le garde")

        if self.couple != None:
            self.couple.role.mort(VIVANTS)
            VIVANTS.remove(self.couple)

class Sorciere:
    """Le rôle de la sorcière"""
    def __str__(self):
        return "Sorcière"

    def __init__(self, joueur):
        self.soi = joueur
        self.vie = 1
        self.mort = 1
        self.couple = None

    async def informe(self):
        await envoi(EMO_ID[self.soi][0], "Tu seras une sorcière pour cette partie")

    async def nuit(self, VIVANTS, PROTECT, VICTIME):
        if self.vie + self.mort != 0:
            txt = f"La victime de cette nuit est {VICTIME[0].nom}\n"
            txt += "Tu peux la sauver\n" if self.vie == 1 else ""
            txt += "Tu peux tuer qqn\n" if self.mort == 1 else ""
            txt += "Indiquer 'sauver' ou le nom de la personne à tuer"
            sonde = await demande(EMO_ID[self.soi][0], txt, 15)
            if sonde != -1:
                if sonde == 'sauver' and self.vie == 1:
                    vict = str(VICTIME[0].nom)
                    VICTIME.pop(0)
                    txt = f"{vict} a été sauvé"
                    self.vie -= 1
                elif self.mort == 1:
                    poss = [x for x in VIVANTS if x.nom_std == sonde]
                    if len(poss) == 1 and not poss[0] in VICTIME:
                        VICTIME.append(poss[0])
                        txt = f"{VICTIME[-1].nom} a été tué"
                        self.mort -= 1

                await envoi(EMO_ID[self.soi][0], txt)

    async def mort(self, VIVANTS):
        channel = CLIENT.get_channel(778578524193030184)
        await channel.send(f"{EMO_ID[self.soi][2]} était la sorcière")

        if self.couple != None:
            self.couple.role.mort(VIVANTS)
            VIVANTS.remove(self.couple)

class Chaceur:
    """Le rôle du chaceur"""
    def __str__(self):
        return "Chaceur"

    def __init__(self, joueur):
        self.soi = joueur
        self.couple = None

    async def informe(self):
        await envoi(EMO_ID[self.soi][0], "Tu seras un chaceur pour cette partie")

    async def nuit(self, VIVANTS, PROTECT, VICTIME):
        return

    async def mort(self, VIVANTS):
        channel = CLIENT.get_channel(778578524193030184)
        await channel.send(f"{EMO_ID[self.soi][2]} était le chaceur, il choisit qui il veut tuer")
        txt = "Tu viens de mourir, choisis qui tu veux emmener dans la tombe avec toi"
        sonde = await demande(EMO_ID[self.soi][0], txt, 15)

        poss = [x for x in VIVANTS if x.nom_std == sonde]
        if sonde != -1 and len(poss) == 1:
            await channel.send(f"Le chaceur a sorti son fusil, a pointé {poss[0].nom} et a tiré")
            poss[0].role.mort(VIVANTS)
            VIVANTS.remove(poss[0])

        if self.couple != None:
            self.couple.role.mort(VIVANTS)
            VIVANTS.remove(self.couple)

class Villageois:
    """Le rôle du villageois"""
    def __str__(self):
        return "Villageois"

    def __init__(self, joueur):
        self.soi = joueur
        self.couple = None

    async def informe(self):
        await envoi(EMO_ID[self.soi][0], "Tu seras un simple villageois pour cette partie (RIP)")

    async def nuit(self, VIVANTS, PROTECT, VICTIME):
        return

    async def mort(self, VIVANTS):
        channel = CLIENT.get_channel(778578524193030184)
        await channel.send(f"{EMO_ID[self.soi][2]} était un simple villageois")

        if self.couple != None:
            self.couple.role.mort(VIVANTS)
            VIVANTS.remove(self.couple)

class Cupidon:
    """Le rôle du villageois"""
    def __str__(self):
        return "Cupidon"

    def __init__(self, joueur):
        self.soi = joueur
        self.couple = None
        self.nuit = True

    async def informe(self):
        await envoi(EMO_ID[self.soi][0], "Tu seras cupidon pour cette partie (Vive l'amour)")

    async def nuit(self, VIVANTS, PROTECT, VICTIME):
        if self.nuit:
            txt = "Qui sera la première personne du couple ?"
            while 1:
                sonde = await demande(EMO_ID[self.soi][0], txt, 7)
                mari = [x for x in VIVANTS if x.nom_std == sonde]
                if len(mari) == 1:
                    break

            txt = "Et la seconde ?"
            while 1:
                sonde = await demande(EMO_ID[self.soi][0], txt, 7)
                femme = [x for x in VIVANTS if x.nom_std == sonde]
                if len(femme) == 1:
                    break
                    
            femme[0].couple = mari[0]
            mari[0].couple = femme[0]

            self.nuit = False

    async def mort(self, VIVANTS):
        channel = CLIENT.get_channel(778578524193030184)
        await channel.send(f"{EMO_ID[self.soi][2]} était le cupidon")

        if self.couple != None:
            self.couple.role.mort(VIVANTS)
            VIVANTS.remove(self.couple)


class Loup:
    """Le rôle du loup"""
    def __str__(self):
        return "Loup"

    def __init__(self, joueur):
        self.soi = joueur
        self.couple = None

    async def informe(self):
        await envoi(EMO_ID[self.soi][0], "Tu seras un loup pour cette partie")

    async def nuit(self, VIVANTS, PROTECT, VICTIME):
        id_loups = [x.iden for x in VIVANTS if str(x.role) == 'Loup']
        txt = "Qui veux-tu manger cette nuit ?\n(Si aucun nom de victime n'est majoritaire, "
        txt += "le choix se fera entre les plus cités)"
        L = await asyncio.gather(*[demande(iden, txt, 30) for iden in id_loups])
        noms = [x.nom_std for x in VIVANTS if str(x.role) != 'Loup']
        res = []
        for elt in noms:
            res.append(L.count(elt))
        indices = indices_maximums(res)
        if len(indices) == 1:
            VICTIME.append([x for x in VIVANTS if x.nom_std == noms[indices[0]]][0])
        else:
            indice = choice(indices)
            VICTIME.append([x for x in VIVANTS if x.nom_std == noms[indice]][0])

    async def mort(self, VIVANTS):
        channel = CLIENT.get_channel(778578524193030184)
        await channel.send(f"{EMO_ID[self.soi][2]} était un loup")

        if self.couple != None:
            self.couple.role.mort(VIVANTS)
            VIVANTS.remove(self.couple)


JOUEURS = [[]]
CONFIG_ACTU = [[]]

ROLES = {'villageois' : Villageois, 'loup' : Loup, 'sorciere' : Sorciere, 'garde' : Garde,
         'voyante' : Voyante, 'chaceur' : Chaceur}
         #'cocktailiste' : Cocktailiste, 'cupidon' : Cupidon}
ORDRE_NUIT = [['Garde', 'Voyante', 'Loup', 'Sorciere']]
        # 'Cupidon',                                'Cocktailiste'

NUIT_DEB = {'Garde'    : "Le garde sent que quelque chose de tragique se prépare, il se réveille en sursaut",
            'Voyante'  : "La voyante, ouvre, en plus de ses deux yeux, son troisième oeil",
            'Loup'     : "Les loups, affamés, se réveillent et se rejoignent à l'écart du village pour prévoir leur meurtre",
            'Sorcière' : "La sorcière a entendu du bruit cette nuit, elle décide de faire usage de potions"}

NUIT_FIN = {'Garde'    : "Le garde a brandi son bouclier dans la nuit, il se rendort plus serein",
            'Voyante'  : "La voyante a vu et peut a présent dormir sur ses deux oreilles",
            'Loup'     : "Les loups sont repus et peuvent retourner chez eux pour dormir",
            'Sorcière' : "La sorcière est contente de son choix, elle se rendort"}

class Joueur:
    def __init__(self, rol, nom_std):
        self.role = ROLES[rol](nom_std)
        self.iden = EMO_ID[nom_std][0]
        self.emoji = EMO_ID[nom_std][1]
        self.nom = EMO_ID[nom_std][2]
        self.nom_std = nom_std
        self.maire = False


def indices_maximums(liste, *, key=lambda x: x):
    """Retourne la liste des indices des maximums de la liste"""
    maxi, indices = -1, []
    for k, elt in enumerate(liste):
        if key(elt) > maxi:
            maxi, indices = key(elt), [k]
        elif key(elt) == maxi:
            indices.append(k)
    return indices

def standardisation(chaine):
    """Supprime les majuscules et les accents de la chaine donnée"""
    chaine = chaine.lower()
    chaine = chaine.replace('é', 'e')
    return chaine


async def demande(ident, txt, temps):
    """Envoie un message perso à la personne correspondant à l'id et retourne sa réponse"""
    mess_priv = await CLIENT.get_user(ident).send(txt)
    time.sleep(temps)

    k = 0
    async for message in mess_priv.channel.history():
        k += 1
        if standardisation(message.content) in list(EMO_ID.keys()) + ['sauver']:
            return standardisation(message.content)
        if k > 2:
            return -1

async def envoi(ident, txt):
    """Envoie le texte du message à la personne sanss rien attendre en retour"""
    mess_priv = await CLIENT.get_user(ident).send(txt)

async def delall():
    """Supprime tous les messages du channel"""
    n = 0
    channel = CLIENT.get_channel(778578524193030184)
    async for message in channel.history():
        await message.delete()
        n += 1
    if n == 1:
        quit()
    await channel.send(f"Perso je m'arrête là bro ({n} messages supprimés)")
    await delall()

async def mates_loup(VIVANTS):
    """Indique à tous les loups qui sont les loups dans la game"""
    noms_loups = [x.nom for x in VIVANTS if str(x.role) == 'Loup']
    txt = "Les loups de cette partie sont : "
    txt += ', '.join(noms_loups) + '.'
    id_loups = [x.iden for x in VIVANTS if str(x.role) == 'Loup']
    for elt in id_loups:
        await envoi(elt, txt)

async def vote(VIVANTS, choix_du_maire=False):
    """Effectue le vote (retourne la liste des nouveaux vivants après le vote, et le mort)"""
    channel = CLIENT.get_channel(778578524193030184)
    shuffle(VIVANTS)
    MAIRE = [x for x in VIVANTS if x.maire][0] if not choix_du_maire else -1

    texte = "C'est l'heure du vote : 2mn avant la récupération des votes\n\nPour voter pour"   \
            + "quelqu'un, réagissez avec l'emoji lui corrspondant (1 vote maxi par personne svp)\n"
    for personne in VIVANTS:
        texte += f"\t - {personne.nom} : {personne.emoji}\n"

    sond_mess = await channel.send(texte)

    for personne in VIVANTS:
        await sond_mess.add_reaction(personne.emoji)

    time.sleep(2)
    await channel.send('Plus que 1 minute')
    time.sleep(1)
    await channel.send('10s !!')
    time.sleep(1)
    await channel.send('Le vote est terminé')

    async for message in channel.history():
        if message.id == sond_mess.id:
            sond_mess = message

    resultats = []

    for reaction in sond_mess.reactions:
        resultats.append((reaction.count - 1, str(reaction.emoji)))
    indices = indices_maximums(resultats, key=lambda x: x[0])

    if choix_du_maire:              # C'est l'élection du maire (tour 1 seulement du coup)
        if len(indices) == 1:
            VIVANTS[indices[0]].maire == True
            await channel.send(f'{VIVANTS[indices[0]].nom} a été élu maire')

        else:
            await channel.send('Le maire est donc choisi aléatoirement entre les majoritaires')
            choix = choice(indices)
            VIVANTS[choix].maire = True
            await channel.send(f'{VIVANTS[choix].nom} a été élu maire')

        return VIVANTS


    if len(indices) == 1:                   # Une personne sort du lot lors du vote
        txt = VIVANTS[indices[0]].nom
        txt += ', le village a décidé de vous éliminer et la sentence est irrévocable'
        await channel.send(txt)
        pers.role.mort(VIVANTS)
        pers = VIVANTS.pop(indices[0])

    else:              # Il y a égalité entre plusieurs personnes et le maire doit faire son choix
        await channel.send('Il y a égalité entre plusieurs personnes : le maire fait son choix')

        txt = 'Fais ton choix entre :\n'
        for ind in indices:
            txt += f"\t - {VIVANTS[ind].nom}\n"
        txt += "(Répondre ici le nom de la personne à tuer, 15s pour choisir)\n"
        txt += "Si aucun choix n'est fait / le choix n'est pas valide, le résultat sera aléatoire"

        choix = await demande(MAIRE.iden, txt, 15)

        for elt in VIVANTS:
            if elt.nom_std == choix:
                pers = elt

        if choix != -1:
            pers.role.mort(VIVANTS)
            VIVANTS.remove(pers)
            txt = pers.nom
            txt += ', le village a décidé de vous éliminer et la sentence est irrévocable'
            await channel.send(txt)

        else:
            choix = choice(indices)
            pers = VIVANTS.pop(choix)
            pers.role.mort(VIVANTS)
            txt = pers.nom
            txt += ', le village a décidé de vous éliminer et la sentence est irrévocable'
            await channel.send(txt)


    if pers.maire:              # La personne éliminée était le maire
        channel.send("Le maire a été tué, il choisit qui sera son successeur")
        txt = 'Qui doit te succéder comme maire ?\n'
        txt += "(Répondre ici le nom de la personne qui doit te succéder, 15s pour choisir)\n"
        txt += "Si aucun choix n'est fait/le choix n'est pas valide, le résultat sera aléatoire"
        choix = await demande(pers.iden, txt, 15)
        poss = [x for x in VIAVNTS if VIVANTS.nom_std == choix]
        choix = choix if len(poss) == 1 else choice(VIVANTS).nom_std
        poss = [x for x in VIAVNTS if VIVANTS.nom_std == choix]
        poss[0].maire = True
        txt = f"{poss[0].nom} a été choisi comme nouveau maire (pas très démocratique "
        txt += "mais on est pas en cours de français donc c'est bon)"
        await channel.send(txt)

    return VIVANTS

async def partie(JOUEUR, CONFIG):
    """Effectue la partie avec les joueurs donnés et la configuration définie"""
    channel = CLIENT.get_channel(778578524193030184)
    if len(JOUEUR) != len(CONFIG):
        await channel.send("Le nombre de joueurs ne correspond pas au nombre de rôles...")
        return
    if len(CONFIG) < 2:
        await channel.send("Nombre de joueurs insuffisant pour jouer...")
        return
    shuffle(JOUEURS)
    shuffle(CONFIG_ACTU)
    VIVANTS = [Joueur(CONFIG[k], JOUEUR[k]) for k in range(len(JOUEURS))]
    for elt in VIVANTS:
        await elt.role.informe()
    await mates_loup(VIVANTS)
    tour = 1
    txt = "Je vais vous raconter l'histoire d'un village ancien. Dans ce village vivèrent "
    txt += "tranquillement des villageois jusqu'au jour où le pouvoir du scénario arriva et donna"
    txt += " des capacités à certains de ces villageois et en transforma d'autres en loups-garous."
    txt += "\nLa couille dans le potage, c'est que les loups-garous sont pas ultra gentils et bon,"
    txt += " on va pas se mentir, ils ont faim les cons..."
    await channel.send(txt)
    while 1:
        await channel.send(f"Le village s'endort  (nuit {tour})")
        VICTIME, PROTECT = [], []
        for elt in ORDRE_NUIT[0]:
            poss = [x for x in VIVANTS if str(x.role) == elt]
            if len(poss) != 0:
                await channel.send(NUIT_DEB[elt])
                await poss[0].role.nuit(VIVANTS, PROTECT, VICTIME)
                await channel.send(NUIT_FIN[elt])
        await channel.send('Le soleil se lève, le village se réveille, et cette nuit,')
        mort = 0
        for elt in VICTIME:
            if not elt in PROTECT:
                mort += 1
                elt.role.mort(VIVANTS)
                VIVANTS.remove(elt)
        if mort == 0:
            await channel.send("personne n'est mort (noice)")

        fin = await fin_du_game(VIVANTS)

        if fin:
            return

        if tour == 1:
            await channel.send("C'est l'heure d'élire le maire du village")
            VIVANTS = await vote(VIVANTS, choix_du_maire=True)

        await channel.send("Et, c'est parti pour un vote, l'ambiance devient délétaire au village")
        VIVANTS = await vote(VIVANTS)

        fin = await fin_du_game(VIVANTS)

        if fin:
            return

        tour += 1

def gagne_loups(VIVANTS):
    """Indique si les loups ont gagné"""
    for elt in VIVANTS:
        if str(elt.role) != 'Loup':
            return False
    return True

def gagne_village(VIVANTS):
    """Indique si le village a gagné"""
    ROLES_VILLAGE = ["Villageois", "Sorcière", "Voyante", "Garde", "Chaceur"]
    for elt in VIVANTS:
        if not str(elt.role) in ROLES_VILLAGE:
            return False
    return True

def gagne_couple(VIVANTS):
    """Indique si le couple désigné par cupidon à gagné"""
    for elt in VIVANTS:
        if elt.couple == None:
            return False
    return True

async def fin_du_game(VIVANTS):
    """Indique si une des teams à gagné"""
    if gagne_loups(VIVANTS):
        await channel.send("Victoire des loups")
        return True
    
    if gagne_village(VIVANTS):
        await channel.send("Victoire du village")
        return True
    
    if gagne_couple(VIVANTS):
        await channel.send("Victoire du couple")
        return True


# --------------------------------------------------------------------------------------------------
async def test():
    channel = CLIENT.get_channel(778578524193030184)
    await channel.send('Pas de test en cours...')

# --------------------------------------------------------------------------------------------------

@CLIENT.event
async def on_ready():
    """Active le bot"""
    print('Bot logged in as {0.user}'.format(CLIENT))
    await CLIENT.change_presence(activity=discord.Game("faire des tests"))
    channel = CLIENT.get_channel(778578524193030184)
    message = await channel.send("🐺 Le bot est opérationnel 🐺")


@CLIENT.event
async def on_message(message):
    """Réaction à un message"""
    channel = message.channel

    if str(channel) == 'loup-garou' or str(channel)[:6] == 'Direct':
        print(message.author, channel, CLE, message.content)

        if message.content != '!test' and message.author == CLIENT.user:
            return

        # Commande delall
        if str(message.author) == "Solénoide#8521" and message.content == CLE + 'OnDégageTtMessage':
            await message.delete()
            await delall()

        # Commande !suggest
        if message.content[:8] == CLE + 'suggest':
            with open("idées.txt", 'a') as fichier:
                fichier.write(str(message.author) + '\n' + message.content[8:] + '\n\n')
            await message.delete()
            await channel.send('Merci pour cette idée')

        # Commande !seeconfig
        if message.content[:10] == CLE + 'seeconfig':
            n = int(message.content[11])
            txt = f'Les configurations à {n} joueurs sont :\n'
            for m, elt in enumerate(CONFIGS[n]):
                txt += str(m) + (4 - len(str(m))) * ' ' + '->  '
                for e in elt:
                    txt += e + ', '
                txt = txt[:-2] + '\n'
            await channel.send(txt)

        # Commande !disporoles
        if message.content[:11] == CLE + 'disporoles':
            txt = 'Les rôles disponibles sont '
            txt += ', '.join(ROLES.keys())
            await channel.send(txt + '.')

        # Commande !test
        if message.content[:5] == CLE + 'test':
            await test()

        # Commande !help
        if message.content[:5] == CLE + 'help':
            with open('instruc.txt', 'r') as fichier:
                txt = fichier.readlines()
            await channel.send(''.join(txt))

        # Commande !addjoueur
        if message.content[:10] == CLE + 'addjoueur':
            std = standardisation(message.content[11:])
            if not std in JOUEURS[0] and std in EMO_ID.keys():
                JOUEURS[0].append(std)
                await channel.send("Joueur ajouté")

        # Commande !deljoueur
        if message.content[:10] == CLE + 'deljoueur':
            try:
                JOUEURS[0].remove(standardisation(message.content[11:]))
                await channel.send("Joueur supprimé")
            except:
                None

        # Commande !joueurs
        if message.content[:8] == CLE + 'joueurs':
            txt = 'Les joueurs actuels sont : '
            for elt in JOUEURS[0]:
                txt += EMO_ID[elt][2] + ', '
            await channel.send(txt[:-2] + '.')

        # Commande !config
        if message.content == CLE + 'config':
            txt = 'Les rôles de la configuration actuelle sont : '
            txt += ', '.join(CONFIG_ACTU[0])
            await channel.send(txt + '.')

        # Commande !setconfig
        if message.content[:10] == CLE + 'setconfig':
            print(message.content[11], '.', message.content[13])
            try:
                CONFIG_ACTU[0] = list(CONFIGS[int(message.content[11])][int(message.content[13])])
                await channel.send('La configuration a été modifiée')
            except:
                None

        # Commande !addrole
        if message.content[:8] == CLE + 'addrole':
            if standardisation(message.content[9:]) in ROLES.keys():
                CONFIG_ACTU[0].append(standardisation(message.content[9:]))
                await channel.send("Le rôle a été ajouté à la configuration")

        # Commande !delrole
        if message.content[:8] == CLE + 'delrole':
            try:
                CONFIG.remove(standardisation(message.content[9:]))
                await channel.send("Le rôle a été enlevé de la configuration")
            except:
                None

        # Commande !getnew
        if message.content[:7] == CLE + 'getnew':
            important = message.content.split()[1:]
            txt = f"'{standardisation(important[1])}' : ("
            txt += important[0][3:-1] + ', ' + important[2] + ', ' + important[1] + ')'
            print(txt)
            await channel.send("La chaine a été créée, redémarrage...")
            quit()

        # Commande !lancerpartie
        if message.content[:13] == CLE + 'lancerpartie':
            await partie(JOUEURS[0], CONFIG_ACTU[0])


CLIENT.run(TOKEN)

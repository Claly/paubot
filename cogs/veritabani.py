import os
import random

import discord
import sqlite3
import datetime
from discord.ext import commands
from prettytable import PrettyTable

random_isim = ["Talha","Hakan","Mete","Deniz","Yüksel","Sabiha","Safiye","Ali","Emre","Mert","Sema","Merve","Burcu","Aysel","Hülya","Hüseyin","Zeynep","Hanife","Cihat","Ramazan","Remzi","Şefik","Faik","Oya","İpek","Merve","Tuana","Sena","Sema","Aslı","Duygu","Ceren","Hazal","Hazel","Sıddık","Ebubekir","Ali Efe","Mehmet Ali","Muhammed Ömer","Ömer Faruk"]
random_meslek = ["Doktor","Avukat","Kuaför","Esnaf","Serbest Meslek","İnşaatçı","Emlakçı","Mühendis","Bakkal","Motokurye","Veteriner","Diş Hekimi","Öğretmen","Hademe","Müdür","Çiftçi","Aşçı","Polis","Galerici","Asker","Sporcu", "Pornocu"]

class veritabani(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return
        ignored = (commands.CommandNotFound, )
        error = getattr(error, 'original', error)
        if isinstance(error, ignored):
            return

        if isinstance(error, sqlite3.OperationalError):
            embed = discord.Embed(title=":x: Bir hata oluştu", description=f"Hata Açıklaması\n```{error}```", color=0xff8585)
            await ctx.send(embed=embed)
    @commands.command(name='Database', aliases=['db'])
    async def db(self, ctx, *, arg1="31"):
        """Veritabanı işlemleri için"""
        embed = discord.Embed(colour=0x46adfb, description="Veritabanı işlemlerini gerçekleştirmek için hazırlanan bir komut\n**Kullanım**: `.<komut>`\n**Örnek**: `.ornek-tablo`", timestamp=datetime.datetime.utcnow())

        embed.set_thumbnail(url="https://miro.medium.com/max/512/1*erh9SXN7CxL73IBu_6whsw.png")
        embed.set_author(name="Veritabanı Yardım", icon_url="https://www.freepnglogos.com/uploads/question-mark-png/red-and-yellow-question-mark-transparent-png-svg-vector-4.png")
        embed.set_footer(text="PAÜ", icon_url="https://upload.wikimedia.org/wikipedia/tr/archive/5/5b/20161212145104%21Pamukkale_%C3%9Cniversitesi.png")

        embed.add_field(name="Komutlar :coffee: ", value="`ornek-tablo`\n`tablo-olustur`\n`sql-sorgu`\n`sql-tablolarim`", inline=True)
        embed.add_field(name="Açıklama :book: ", value="Örnek tablo oluşturur\nTablo oluşturur\nTabloda sql sorgusu yapar\nSql tablolarınızı gösterir", inline=True)

        await ctx.send(embed=embed)

    @commands.command(name='sql-tablolarim', aliases=['st',"sql-tablo"])
    async def tablo_liste(self, ctx):
        dbname = f"databases/{ctx.author.id}.db"
        con = sqlite3.connect(dbname)
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablolar = cur.fetchall()
        _tablolar = []
        y = 1
        for x in tablolar:
            _tablolar.append("[ " + str(y) + " ] - " + str(x).replace("(","").replace(")","").replace(",","").replace("'",""))
            y += 1
        _fieldtext = "\n".join(_tablolar)
        embed = discord.Embed(title="SQL Sorgusu", description=f"Toplam **{len(_tablolar)} adet** tablo var", color=0x5d95a8)
        embed.set_thumbnail(url="https://www.pentarray.com/wp-content/uploads/2018/02/database-logo.png")
        embed.add_field(name="Tablolar", value=f"```glsl\n{_fieldtext}```", inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='ornek-tablo', aliases=['ot'])
    async def ornek_tablo(self, ctx):
        dbname = f"databases/{ctx.author.id}.db"
        self.db_olustur(dbname)
        con = sqlite3.connect(dbname)
        cur = con.cursor()
        cur.execute('''
                    CREATE TABLE ornek(
                       ID INTEGER PRIMARY KEY,
                       isim varchar(255) NOT NULL,
                       yas int NOT NULL,
                       meslek varchar(255) NOT NULL,
                       aylik_kazanc int NOT NULL
                       
                    );''')

        _isim = random_isim
        for x in range(1,21):
            gecici = random.choice(_isim)
            meslek = random.choice(random_meslek)
            maas = random.randrange(5000,15000,100)
            cur.execute(f"INSERT INTO ornek ('isim','yas','meslek','aylik_kazanc') VALUES ('{gecici}','{random.randint(24,70)}','{meslek}','{maas}')")
            _isim.remove(gecici)
        con.commit()
        con.close()

    def db_olustur(self,dbname):
        if not os.path.isfile(dbname):
            open(dbname,"w")
def setup(bot):
    bot.add_cog(veritabani(bot))

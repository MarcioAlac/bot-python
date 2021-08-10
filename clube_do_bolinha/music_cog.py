import discord
from discord.ext  import commands
from  youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  
        self.is_playing = False # verifica se a musica está tocando ou nao 
        self.music_queue = []  # fila de musicas pedidas 
        
        self.YDL_OPTIONS = {'format':'bestaudio', 'noplaylist':True} # atributos 
        self.FFMPEG_OPTIONS = {'before_options': "-reconnect 1 reconnect_streamed 1 -reconnect_delay_max 5", 'options': '-vn'}
        
        self.vc = ""

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch: %s" % item, download= False)['entries'][0]
            except Exception:
                return False

            return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after= lambda e: self.play_next())

        else:
            self.is_playing = False

    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            
            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])
                

            print(self.music_queue) 
            self.music_queue.pop()

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after= lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="tocar", help="Tocando seleção do youtube")
    async def  p(self, ctx, *args):
        query = " ".join(args)
      
        channel = ctx.message.author.voice.channel

        if channel is None:
            await ctx.send("Conecte ao chate de voz")
        else:
            song = self.search_yt(query)

            if type(song) == type(True):
                await ctx.send("O som nao pode ser streemado, tente outro nome ou verifique se o nome está correto")
            else:
                await ctx.send("Tocando a musica selecionada")
                self.music_queue.append([song, channel])
            
            if self.is_playing == False:
                await self.play_music()

    @commands.command(name="fila", help="A musica ja esta na fila")
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"

        print(retval)
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("Nenhuma musica na fila")

    @commands.command(name="pular", help="Pulando musica atual")
    async def pular(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            await self.play_music()
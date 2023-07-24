import difflib

from twitchio.ext import commands


class SatisfactoryCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.all_commands = {
            "get_colors": "Input a named item from Satisfactory to get its colors.",
        }

    @commands.command()
    @commands.cooldown(5, 60)
    async def get_colors(self, ctx: commands.Context, item_name: str = None):
        color_dict = {
            "Iron Ore": ("663633", "656f8c"),
            "Copper Ore": ("9d5a47", "405a61"),
            "Caterium Ore": ("e9d2a0", "a27a40"),
            "Limestone": ("c6b5ab", "89765f"),
            "Coal": ("050807", "0b0f15"),
            "Sulfur": ("ded267", "876421"),
            "Raw Quartz": ("ed82bc", "9d2a68"),
            "Bauxite": ("d29a80", "9c5548"),
            "Uranium Ore": ("448a3a", "173717"),
            "Leaves": ("4d6f43", "142c12"),
            "Wood": ("735e43", "2a1e14"),
            "Biomass": ("6b5f35", "3e3118"),
            "Solid Biofuel": ("847161", "3c2f25"),
            "Mycelia": ("8b8186", "3e3c49"),
            "Flower Petals": ("a94066", "7d8398"),
            "Fabric": ("978a85", "000003"),
            "Concrete": ("83755f", "c7c3c8"),
            "Iron Ingot": ("8e9298", "484948"),
            "Iron Plate": ("afb2b6", "4c4f54"),
            "Iron Rod": ("595b63", "1c1a22"),
            "Screw": ("99a2aa", "1164ce"),
            "Reinforced Iron Plate": ("9aa2b5", "59657e"),
            "Modular Frame": ("838baa", "5d5d5d"),
            "Copper Ingot": ("b07e7c", "553329"),
            "Copper Sheet": ("9e6d63", "325a8d"),
            "Wire": ("ab6c47", "846b4f"),
            "Cable": ("282a32", "6b6862"),
            "Copper Powder": ("7d5664", "afa4b6"),
            "Stator": ("444351", "59352c"),
            "Motor": ("47526f", "bf971f"),
            "Heavy Modular Frame": ("818896", "1b1b1b"),
            "Smart Plating": ("464b73", "a34033"),
            "Automated Wiring": ("26292e", "a34033"),
            "Caterium Ingot": ("cdba89", "927844"),
            "Quickwire": ("cdba89", "2a2e3f"),
            "Rotor": ("364364", "744029"),
            "Quartz Crystal": ("cb86c9", "3150b4"),
            "Silica": ("d3d4dd", "b2cedf"),
            "Crystal Oscillator": ("f7cf4e", "999198"),
            "Circuit Board": ("2b5533", "ffb85f"),
            "High-Speed Connector": ("2b5533", "415355"),
            "Steel Ingot": ("23272c", "0f1011"),
            "Steel Beam": ("292a2e", "703d30"),
            "Steel Pipe": ("323232", "703d30"),
            "Encased Industrial Beams": ("b3a891", "863f40"),
            "Versatile Framework": ("292a2d", "8b2819"),
            "Computer": ("c08e5a", "2e3531"),
            "Modular Engine": ("45444b", "a34033"),
            "Adaptive Control Unit": ("6b686c", "dfa05a"),
            "Assembly Director System": ("303032", "a34033"),
            "Magnetic Field Generator": ("303032", "9ad7b1"),
            "Nuclear Pasta": ("c08e5a", "93f8f7"),
            "Thermal Propulsion Rocket": ("303032", "a34033"),
            "Water": ("1f7ca1", "0d0d0e"),
            "Packaged Water": ("66a5c6", "0251b8"),
            "Crude Oil": ("111112", "0d0d0e"),
            "Packaged Crude Oil": ("0d0d0e", "d5d4d2"),
            "Heavy Oil Residue": ("85019a", "0d0d0e"),
            "Packaged Heavy Oil Residue": ("85019a", "d5d4d2"),
            "Fuel": ("cd812b", "0d0d0e"),
            "Packaged Fuel": ("f9a320", "10100e"),
            "Liquid Biofuel": ("263e1a", "0d0d0e"),
            "Packaged Liquid Biofuel": ("195200", "10100e"),
            "Turbofuel": ("810006", "0d0d0e"),
            "Packaged Turbofuel": ("d60710", "10100e"),
            "Empty Canister": ("64606a", "10100e"),
            "Alumina Solution": ("b4b1b7", "0d0d0e"),
            "Packaged Alumina Solution": ("bdc0cc", "dcaf4c"),
            "Sulfuric Acid": ("d1c83a", "0d0d0e"),
            "Packaged Sulfuric Acid": ("b2ae4f", "42434f"),
            "Nitric Acid": ("d8d8bc", "0d0d0e"),
            "Nitrogen Gas": ("b0acb4", "0d0d0e"),
            "Packaged Nitrogen Gas": ("23273b", "b7b9c6"),
            "Packaged Nitric Acid": ("cfcfdb", "454550"),
            "Plastic": ("4dacf2", "221f24"),
            "Polymer Resin": ("252fd4", "060330"),
            "Rubber": ("1e1d1d", "cfb65e"),
            "Petroleum Coke": ("2b2c34", "060602"),
            "Empty Fluid Tank": ("7b95bd", "99969b"),
            "Compacted Coal": ("171a24", "0d0c09"),
            "Black Powder": ("1c1d23", "c8000a"),
            "Smokeless Powder": ("0c0c0c", "df1720"),
            "AI Limiter": ("1c1c1a", "648d8c"),
            "Supercomputer": ("222327", "f1bf74"),
            "Radio Control Unit": ("2b2b2b", "e2bc26"),
            "Heat Sink": ("949796", "a1663e"),
            "Battery": ("2d3146", "adadbc"),
            "Fused Modular Frame": ("a5a5a6", "f4aa53"),
            "Cooling System": ("de9860", "999da1"),
            "Turbo Motor": ("2c3034", "cfa011"),
            "Quantum Computer": ("1f1f1f", "e6b16d"),
            "Pressure Conversion Cube": ("d49058", "1f2133"),
            "Superposition Oscillator": ("adaea0", "edc888"),
            "Aluminum Scrap": ("abaaae", "c6841c"),
            "Aluminum Ingot": ("b9bcc3", "666a6c"),
            "Alclad Aluminum Sheet": ("afb2bc", "818073"),
            "Aluminum Casing": ("aaa9ae", "1f2228"),
            "Encased Uranium Cell": ("d8d11b", "8beac3"),
            "Non-fissile Uranium": ("e7e334", "8beac3"),
            "Uranium Fuel Rod": ("1e1e15", "64c987"),
            "Nuclear Waste": ("d9d423", "1cb83b"),
            "Plutonium Pellet": ("758b8f", "72bacd"),
            "Encased Plutonium Cell": ("2b3230", "a8e5e9"),
            "Plutonium Fuel Rod": ("cebe40", "a8e5e9"),
            "Plutonium Waste": ("b6ac23", "71cae3"),
            "Electromagnetic Control Rod": ("383941", "ede954"),
            "Beryl Nut": ("bba775", "b8cace"),
            "Pale Berry": ("f27954", "b14244"),
            "Bacon Agaric": ("f2e2e2", "d7577c"),
            "Medicinal Inhaler": ("ededec", "47aee1"),
            "Hog Remains": ("a38da8", "554051"),
            "Spitter Remains": ("6c5982", "972e37"),
            "Hatcher Remains": ("454792", "e394ae"),
            "Stinger Remains": ("1a1c20", "a07277"),
            "Alien Protein": ("654368", "c9cbce"),
            "Alien DNA Capsule": ("96949d", "2e3531"),
            "Hard Drive": ("994f29", "313130"),
            "Ficsit Coupon": ("e49246", "e9a86a"),
            "Blade Runners": ("092e57", "050505"),
            "Hazmat Suit": ("d2b763", "424462"),
            "Jetpack": ("ffb85c", "373938"),
            "Hover Pack": ("ffb85c", "373938"),
            "Gas Mask": ("eda048", "242122"),
            "Gas Filter": ("8e859c", "131211"),
            "Iodine Infused Filter": ("b6881f", "121311"),
            "Build Gun": ("d99427", "24282b"),
            "Color Gun": ("e38f3f", "1c1b1d"),
            "Object Scanner": ("cd7f24", "151517"),
            "Xeno-Zapper": ("e38f32", "383f52"),
            "Xeno-Basher": ("e2872f", "51c1c8"),
            "Rebar Gun": ("2c2d30", "0d0d0e"),
            "Iron Rebar": ("d27e13", "222025"),
            "Shatter Rebar": ("772e6e", "222025"),
            "Stun Rebar": ("017bb2", "222025"),
            "Explosive Rebar": ("a50810", "222025"),
            "Nobelisk Detonator": ("dcc109", "aa0003"),
            "Nobelisk": ("a00509", "f7f420"),
            "Gas Nobelisk": ("5b7a29", "fcda40"),
            "Pulse Nobelisk": ("8eaab6", "fcda40"),
            "Cluster Nobelisk": ("f39f26", "fb6f58"),
            "Nuke Nobelisk": ("424d49", "72c48a"),
            "Rifle": ("faca42", "272728"),
            "Rifle Ammo": ("cc6927", "050504"),
            "Smart Rifle Ammo": ("272a2d", "423a1b"),
            "Turbo Rifle Ammo": ("c12b31", "090807"),
            "Boombox": ("d6953c", "1f2122"),
            "Chainsaw": ("dd832c", "1d202b"),
            "Zipline": ("d48020", "c8b684"),
            "FICSMAS Gift": ("f0c07a", "d92020"),
            "Red FICSMAS Ornament": ("db0108", "7f0000"),
            "Copper FICSMAS Ornament": ("fea318", "844e01"),
            "Iron FICSMAS Ornament": ("ffffff", "9f9b98"),
            "Blue FICSMAS Ornament": ("1dc0e7", "004f78"),
            "Candy Cane": ("ad0000", "ecdccc"),
            "FICSMAS Wonder Star": ("f9dd2c", "d79103"),
            "FICSMAS Bow": ("f13f2c", "c6080c"),
            "FICSMAS Decoration": ("404124", "c6080c"),
            "Actual Snow": ("fde9d0", "cbc4e0"),
            "Snowball": ("f9ebf7", "dcd6e1"),
            "Snowball Pile": ("f9eaf9", "e3cbbb"),
            "Snowman": ("fbebe2", "cf0c13"),
            "Giant FICSMAS Tree": ("322b12", "121607"),
            "FICSMAS Gift Tree": ("5d4b28", "910002"),
            "FICSMAS Wreath": ("704b15", "910002"),
            "FICSMAS Tree Branch": ("8487a3", "6e5b5b"),
            "Power Shard": ("c6712f", "86c0e9"),
            "Blue Power Slug": ("7bbfdd", "6b74ad"),
            "Yellow Power Slug": ("e7b55a", "e79763"),
            "Purple Power Slug": ("df88e5", "b250d0"),
            "SAM Ingot": ("124354", "2c0436"),
            "FICSIT Coffee Cup™": ("bb7c51", "3ea2d3"),
            "'Employee of the Planet' Cup": ("cda44e", "2a2930"),
            "Mercer Sphere": ("010101", "407246"),
            "Somersloop": ("5e0311", "440d39"),
            "Player": ("ccb692", "dd9a5a")
        }

        item_name = difflib.get_close_matches(item_name, color_dict.keys(), n=1)[
            0] if item_name not in color_dict.keys() else item_name

        if item_name is None:
            await ctx.send("get_color usage: !get_color [item_name] [0 or 1]")
        else:
            await ctx.send(
                f"The colors of {item_name} are: #{color_dict[item_name][0]} and #{color_dict[item_name][1]}")


def prepare(bot):
    bot.add_cog(SatisfactoryCommandsCog(bot))
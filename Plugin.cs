using System.Reflection;
using System.Threading;
using BepInEx;
using BepInEx.Logging;
using HarmonyLib;
using Rewired.Demos;
using UnityEngine;

namespace Archipelabro
{
    [BepInPlugin(MyPluginInfo.PLUGIN_GUID, MyPluginInfo.PLUGIN_NAME, MyPluginInfo.PLUGIN_VERSION)]
    public class Plugin : BaseUnityPlugin
    {
        internal static new ManualLogSource Logger;
        internal static Thread mThread;

        public static bool deathLinkPendin = false;

        private void Awake()
        {
            // Plugin startup logic
            Logger = base.Logger;
            Logger.LogInfo($"Plugin {MyPluginInfo.PLUGIN_GUID} is loaded!");

            // Communication with client
            ThreadStart ts = new ThreadStart(CommunicationGameClient.GetInfo);
            mThread = new Thread(ts);
            mThread.Start();

            // Patch all
            var harmony = new Harmony("com.autrui.archipelabro");
            var assembly = Assembly.GetExecutingAssembly();
            harmony.PatchAll();
        }

        private void Update()
        {
            if (Input.GetKeyDown(KeyCode.V))
            {
                HeroController.players[0]._character.Damage(1, DamageType.Bullet, -400, 0, -1, HeroController.players[0]._character, -100, -100);
            }
        }
    }

    [HarmonyPatch(typeof(Player))]
    static class Player_Patch
    {
        [HarmonyPostfix]
        [HarmonyPatch("LateUpdate")]
        static void DoDeathLink_Patch(Player __instance)
        {
            if (Plugin.deathLinkPendin)
            {
                __instance._character.Damage(1, DamageType.Bullet, -400, 0, -1, HeroController.players[0]._character, -100, -100);
                Plugin.deathLinkPendin = false;
            }
        }
    }

    [HarmonyPatch(typeof(TestVanDammeAnim))]
    static class TestVanDammeAnim_Patch
    {
        [HarmonyPostfix]
        [HarmonyPatch("Death")]
        static void SendDeathLink_Patch()
        {
            CommunicationGameClient.sendRequestBuffer.Add("send_DeathLink");
        }
    }
}



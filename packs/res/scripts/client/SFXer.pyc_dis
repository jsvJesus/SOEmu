# Embedded file name: scripts/client/SFXer.py
import sfx
import BigWorld
import Math
from Math import Vector3
from Math import Matrix
from functools import partial
from Helpers.VectorUtils import getTriangleByZ
import random
from Items import ItemsCatalog
import ThrowingData
import ItemsUtils
import Pixie
import FX
SFX_WEAPON_CATALOG = {ItemsCatalog.SFX_MAKAROV_PISTOL: 'sfx/Weapons/pistol_pm_shoot.xml',
 ItemsCatalog.SFX_COLT_1911_PISTOL: 'sfx/Weapons/pistol_colt-1911_shoot.xml',
 ItemsCatalog.SFX_DESERT_EAGLE_PISTOL: 'sfx/Weapons/pistol_desert_shoot.xml',
 ItemsCatalog.SFX_TOKAREV_TT_PISTOL: 'sfx/Weapons/pistol_tokarev-tt_shoot.xml',
 ItemsCatalog.SFX_GLOCK_17_PISTOL: 'sfx/Weapons/pistol_glock-17_shoot.xml',
 ItemsCatalog.SFX_MP5_SMG: 'sfx/Weapons/smg_hk-mp5-sd3_shoot.xml',
 ItemsCatalog.SFX_MP5_K_SMG: 'sfx/Weapons/smg_hk-mp5-k_shoot.xml',
 ItemsCatalog.SFX_PPSH_41_SMG: 'sfx/Weapons/smg_ppsh-41_shoot.xml',
 ItemsCatalog.SFX_SCORPION_VZ61_SMG: 'sfx/Weapons/smg_scorpion-vz61_shoot.xml',
 ItemsCatalog.SFX_MAC_10_SMG: 'sfx/Weapons/smg_mac-10_shoot.xml',
 ItemsCatalog.SFX_SITES_SPECTRE_M4_SMG: 'sfx/Weapons/smg_sites-spectre-m4_shoot.xml',
 ItemsCatalog.SFX_UZI_SMG: 'sfx/Weapons/smg_uzi_shoot.xml',
 ItemsCatalog.SFX_TOZ34_SHOTGUN: 'sfx/Weapons/shotgun_toz-34_shoot.xml',
 ItemsCatalog.SFX_SAIGA_SHOTGUN: 'sfx/Weapons/rifle_sayga_shoot.xml',
 ItemsCatalog.SFX_JACKHAMMER_MK3A1_SHOTGUN: 'sfx/Weapons/shotgun_jackhammer-mk3a1_shoot.xml',
 ItemsCatalog.SFX_MOSSBERG_500_SHOTGUN: 'sfx/Weapons/shotgun_mossberg-500cr_shoot.xml',
 ItemsCatalog.SFX_FRANCHI_SPAS_12_SHOTGUN: 'sfx/Weapons/shotgun_spas-12_shoot.xml',
 ItemsCatalog.SFX_M1014_JSCS_SHOTGUN: 'sfx/Weapons/shotgun_m1014-jscs_shoot.xml',
 ItemsCatalog.SFX_AK74M_RIFLE: 'sfx/Weapons/autogun_ak-74m_shoot.xml',
 ItemsCatalog.SFX_FN_FAL_RIFLE: 'sfx/Weapons/autogun_fn_fal_shoot.xml',
 ItemsCatalog.SFX_FAMAS_RIFLE: 'sfx/Weapons/autogun_famas_shoot.xml',
 ItemsCatalog.SFX_SIG_751_RIFLE: 'sfx/Weapons/autogun_sig-751_shoot.xml',
 ItemsCatalog.SFX_COLT_M16_RIFLE: 'sfx/Weapons/autogun_colt-m16_shoot.xml',
 ItemsCatalog.SFX_HK_G36C_RIFLE: 'sfx/Weapons/autogun_hk-g36c_shoot.xml',
 ItemsCatalog.SFX_AK_74_RIFLE: 'sfx/Weapons/autogun_ak-74_shoot.xml',
 ItemsCatalog.SFX_AK_102_RIFLE: 'sfx/Weapons/autogun_ak-102_shoot.xml',
 ItemsCatalog.SFX_AK_107_RIFLE: 'sfx/Weapons/autogun_ak-107_shoot.xml',
 ItemsCatalog.SFX_AK_47_RIFLE: 'sfx/Weapons/autogun_ak-47_shoot.xml',
 ItemsCatalog.SFX_AUG_A3_RIFLE: 'sfx/Weapons/autogun_aug-a3_shoot.xml',
 ItemsCatalog.SFX_HK_416_RIFLE: 'sfx/Weapons/autogun_hk-416_shoot.xml',
 ItemsCatalog.SFX_COLT_M4A1_RIFLE: 'sfx/Weapons/autogun_colt-m4a1_shoot.xml',
 ItemsCatalog.SFX_OC_14_939_RIFLE: 'sfx/Weapons/autogun_oc-14_shoot_939.xml',
 ItemsCatalog.SFX_OC_14_762_RIFLE: 'sfx/Weapons/autogun_oc-14_shoot_762.xml',
 ItemsCatalog.SFX_SIG_SAUER_551_RIFLE: 'sfx/Weapons/autogun_sig-sauer-551_shoot.xml',
 ItemsCatalog.SFX_RUGER_RIFLE: 'sfx/Weapons/rifle_ruger-mini-14_shoot.xml',
 ItemsCatalog.SFX_M1_GARAND_RIFLE: 'sfx/Weapons/rifle_m1-garand_shoot.xml',
 ItemsCatalog.SFX_SVD_RIFLE: 'sfx/Weapons/sniper_svd_shoot.xml',
 ItemsCatalog.SFX_WALTHER_RIFLE: 'sfx/Weapons/sniper_walther-wa-2k_shoot.xml',
 ItemsCatalog.SFX_BARRETT_M82A3_RIFLE: 'sfx/Weapons/sniper_barrett-m82a3_shoot.xml',
 ItemsCatalog.SFX_MK12_SPR_RIFLE: 'sfx/Weapons/sniper_mk12-spr_shoot.xml',
 ItemsCatalog.SFX_MK48_MACHINEGUN: 'sfx/Weapons/machinegun_mk-48_shoot.xml',
 ItemsCatalog.SFX_PECHENEG_MACHINEGUN: 'sfx/Weapons/machinegun_pecheneg_shoot.xml',
 ItemsCatalog.SFX_AUG_HBAR_MACHINEGUN: 'sfx/Weapons/autogun_aug-a3_shoot.xml',
 ItemsCatalog.SFX_RPG7_LAUNCHER: 'sfx/Weapons/launcher_rpg7_shoot.xml',
 ItemsCatalog.SFX_M79_LAUNCHER: 'sfx/Weapons/launch_m79_shoot.xml',
 ItemsCatalog.SFX_PISTOL_SILENCER: 'sfx/Weapons/Silenced/pistol_silenced_shoot.xml',
 ItemsCatalog.SFX_SHOTGUN_SILENCER: 'sfx/Weapons/Silenced/shotgun_silenced_shoot.xml',
 ItemsCatalog.SFX_ASSAULT_5_SILENCER: 'sfx/Weapons/Silenced/assault_5_silenced_shoot.xml',
 ItemsCatalog.SFX_ASSAULT_762x39_SILENCER: 'sfx/Weapons/Silenced/assault_762x39_silenced_shoot.xml',
 ItemsCatalog.SFX_ASSAULT_7_SILENCER: 'sfx/Weapons/Silenced/assault_7_silenced_shoot.xml',
 ItemsCatalog.SFX_SNIPER_5_SILENCER: 'sfx/Weapons/Silenced/sniper_5_silenced_shoot.xml',
 ItemsCatalog.SFX_SNIPER_7_SILENCER: 'sfx/Weapons/Silenced/sniper_7_silenced_shoot.xml',
 ItemsCatalog.SFX_SPECIAL_9x39_SILENCER: 'sfx/Weapons/Silenced/special_9_silenced_shoot.xml',
 ItemsCatalog.SFX_VAL_VSS_RIFLE: 'sfx/Weapons/autogun_val-vss_shoot.xml',
 ItemsCatalog.SFX_SR3_SHOOT: 'sfx/Weapons/sr3_shoot.xml',
 ItemsCatalog.SFX_SR3_SHOOT_SILENCED: 'sfx/Weapons/sr3_shoot_silenced.xml',
 ItemsCatalog.SFX_NONE: 'sfx/Weapons/none.xml',
 'default': 'sfx/gun_fire.xml'}
Wood, Stone, Chain, Light_Metal, Heavy_Metal, Glass, Dirt, Grass, Snow, Water, Flesh, Plastic, Gravel, Rubber, Stone_Tile, Garbage, Mud, Grass_Wet, Sand = xrange(1, 20)
SFX_HIT_CATALOG = {Wood: 'sfx/Shoot/wood_hit.xml',
 Stone: 'sfx/Shoot/stone_hit.xml',
 Chain: 'sfx/Shoot/chain_hit.xml',
 Light_Metal: 'sfx/Shoot/light_metal_hit.xml',
 Heavy_Metal: 'sfx/Shoot/heavy_metal_hit.xml',
 Glass: 'sfx/Shoot/glass_hit.xml',
 Dirt: 'sfx/Shoot/dirt_hit.xml',
 Grass: 'sfx/Shoot/grass_hit.xml',
 Snow: 'sfx/Shoot/snow_hit.xml',
 Water: 'sfx/Shoot/water_hit.xml',
 Flesh: 'sfx/Shoot/body_hit.xml',
 Plastic: 'sfx/Shoot/plastic_hit.xml',
 Gravel: 'sfx/Shoot/gravel_hit.xml',
 Rubber: 'sfx/Shoot/rubber_hit.xml',
 Stone_Tile: 'sfx/Shoot/stone_tile_hit.xml',
 Garbage: 'sfx/Shoot/garbage_hit.xml',
 Mud: 'sfx/Shoot/mud_hit.xml',
 Grass_Wet: 'sfx/Shoot/grass_wet_hit.xml',
 Sand: 'sfx/Shoot/sand_hit.xml',
 'default': 'sfx/Shoot/default_hit.xml'}

def get_gunfire_sfx_path(sfx_type):
    return SFX_WEAPON_CATALOG.get(sfx_type, SFX_WEAPON_CATALOG['default'])


def GunFire(player, sfx_type):
    sfx_path = get_gunfire_sfx_path(sfx_type)
    FX.bufferedOneShotEffect(sfx_path, player.autogunModel)


def get_shell_launch_sfx(player, mode):
    equippedItemType = ItemsUtils.GetEquippedItemType(player)
    noShellLaunchList = [20,
     10223,
     10224,
     10225,
     10226,
     10247,
     10248,
     10249,
     10250,
     10251,
     10252,
     10253,
     10254,
     10255,
     10256,
     10257,
     10258,
     10259,
     10260,
     10261,
     10262,
     10263,
     10264,
     10265,
     10266]
    noShellOnlyOnShootLaunchList = [8, 21, 26]
    if player.ActiveItemType in noShellLaunchList or player.ActiveItemType in noShellOnlyOnShootLaunchList and mode == ItemsUtils.MODE_FIRE:
        return None
    elif equippedItemType == ItemsCatalog.SHOTGUN or player.ActiveItemType == 21:
        return 'sfx/shell_launch_shotgun.xml'
    elif equippedItemType in [ItemsCatalog.PISTOL, ItemsCatalog.REVOLVER, ItemsCatalog.SUB_MACHINE_GUN]:
        return 'sfx/shell_launch_pistol.xml'
    elif equippedItemType in [ItemsCatalog.ASSAULT_RIFLE,
     ItemsCatalog.SNIPER_RIFLE,
     ItemsCatalog.RIFLE,
     ItemsCatalog.MACHINE_GUN]:
        return 'sfx/shell_launch_autogun.xml'
    else:
        return None
        return None


def ShellLaunch(player, mode):
    sfx_path = get_shell_launch_sfx(player, mode)
    if sfx_path:
        FX.bufferedOneShotEffect(sfx_path, player.autogunModel)


def tri_normal(triangle):
    tri_normal = (triangle[2] - triangle[0]) * (triangle[2] - triangle[1])
    tri_normal.normalise()
    return tri_normal


def Explode(player, shoot_source, shoot_target, shoot_normal, target_triangle, material):
    explosion_model = BigWorld.Model('')
    player.addModel(explosion_model)
    target_normal = tri_normal(target_triangle)
    near_shoot_target = shoot_target + target_normal * 0.1
    v = shoot_normal * Vector3(0, 1, 0)
    explosion_model.alignTriangle(near_shoot_target, near_shoot_target + v * 0.05, near_shoot_target + shoot_normal * v * 0.05, False)
    sfx.bufferedOneShotSFX('sfx/grenade_explode.xml', explosion_model, DecalInfo=[shoot_target - (0, 1, 0), shoot_target + (0, 1, 0)])
    BigWorld.callback(3.3, partial(player.delModel, explosion_model))


def footWaterStep(player, position, sfx_path, alignToVector = None, lifeTime = 3.3):
    explosion_model = BigWorld.Model('')
    explosion_model.position = position
    player.addModel(explosion_model)
    if alignToVector:
        pass
    sfx.bufferedOneShotSFX(sfx_path, explosion_model)
    BigWorld.callback(lifeTime, partial(player.delModel, explosion_model))


def waterHit(player, position, sfx_path, alignToVector = None, lifeTime = 3.3):
    hiden_model = BigWorld.Model('characters/items/weapons/sphere_water_spl.model')
    explosion_model = BigWorld.Model('')
    explosion_model.position = position
    hiden_model.position = position + Math.Vector3(0, 1, 0)
    player.addModel(explosion_model)
    player.addModel(hiden_model)
    if alignToVector:
        pass

    def dwn():
        hiden_model.position = position + Math.Vector3(0, -1, 0)

    sfx.bufferedOneShotSFX(sfx_path, explosion_model)
    BigWorld.callback(0.1, dwn)
    BigWorld.callback(lifeTime, partial(player.delModel, explosion_model))
    BigWorld.callback(lifeTime, partial(player.delModel, hiden_model))


def Ricochet(player, shoot_source, shoot_target, target_triangle, material):
    ricochet_model = BigWorld.Model('')
    player.addModel(ricochet_model)
    target_normal = tri_normal(target_triangle)
    ricochet_model.alignToVector(target_normal, shoot_target, False)
    if material in SFX_HIT_CATALOG:
        sfx_hit_name = SFX_HIT_CATALOG[material]
    else:
        sfx_hit_name = SFX_HIT_CATALOG['default']
    sfx.bufferedOneShotSFX(sfx_hit_name, ricochet_model, DecalInfo=[shoot_target + target_normal, shoot_target - target_normal])
    BigWorld.callback(2.0, partial(player.delModel, ricochet_model))


def BodyHit(hitPos, entity, shoot_normal, reflection, sfx_path = 'sfx/Shoot/body_hit.xml'):
    hit_model = BigWorld.Model('')
    entity.addModel(hit_model)
    target_triangle = []
    triangle = getTriangleByZ(reflection)
    for AnglesNum in xrange(len(triangle)):
        target_triangle.append(triangle[AnglesNum] + hitPos)

    hit_model.alignTriangle(target_triangle[0], target_triangle[1], target_triangle[2], False)
    back_normal = Vector3(shoot_normal)
    hit_height = hitPos[1]
    hit_height -= hit_height / (random.random() * 3.0)
    height_shift_vector = Vector3(0, hit_height, 0)
    back_normal -= height_shift_vector
    back_normal = back_normal.scale(5)
    sfx.bufferedOneShotSFX(sfx_path, hit_model, DecalInfo=[hitPos, hitPos + back_normal])
    BigWorld.callback(1.0, partial(entity.delModel, hit_model))


def ArmorNotBroken(hitPos, entity, reflection):
    hit_model = BigWorld.Model('')
    entity.addModel(hit_model)
    target_triangle = []
    triangle = getTriangleByZ(reflection)
    for AnglesNum in xrange(len(triangle)):
        target_triangle.append(triangle[AnglesNum] + hitPos)

    hit_model.alignTriangle(target_triangle[0], target_triangle[1], target_triangle[2], False)
    sfx.bufferedOneShotSFX('sfx/Shoot/armor_hit.xml', hit_model)
    BigWorld.callback(1.0, partial(entity.delModel, hit_model))


def JumpEffect(entity, delay = 0.0):

    def callback_func():
        sfx.bufferedOneShotSFX('sfx/Player/jump.xml', entity.model)

    if delay:
        BigWorld.callback(delay, callback_func)
    else:
        callback_func()


def JumpEndEffect(entity, delay = 0.0):

    def callback_func():
        sfx.bufferedOneShotSFX('sfx/Player/landing.xml', entity.model)

    if delay:
        BigWorld.callback(delay, callback_func)
    else:
        callback_func()


def FlashlightSwitch(entity, delay = 0.0):

    def callback_func():
        sfx.bufferedOneShotSFX('sfx/items/flashlight.xml', entity.model)

    if delay:
        BigWorld.callback(delay, callback_func)
    else:
        callback_func()


def DeathEffect(entity, delay = 0.0):

    def callback_func():
        sfx.bufferedOneShotSFX('sfx/Player/death.xml', entity.model)

    if delay:
        BigWorld.callback(delay, callback_func)
    else:
        callback_func()


def ReloadEffect(entity, sx_name, delay = 0.0):

    def callback_func():
        sfx.bufferedOneShotSFX(sx_name, entity.model)

    if delay:
        BigWorld.callback(delay, callback_func)
    else:
        callback_func()


def RepairEffect(entity, delay = 0.0):

    def callback_func():
        pass

    if delay:
        BigWorld.callback(delay, callback_func)
    else:
        callback_func()


def EatEffect(entity, delay = 0.0):

    def callback_func():
        pass

    if delay:
        BigWorld.callback(delay, callback_func)
    else:
        callback_func()


def HealEffect(entity, delay = 0.0):

    def callback_func():
        pass

    if delay:
        BigWorld.callback(delay, callback_func)
    else:
        callback_func()


def ChangeStanceEffect(entity, delay = 0.0):

    def callback_func():
        pass

    if delay:
        BigWorld.callback(delay, callback_func)
    else:
        callback_func()


def WeaponEquipEffect(entity, delay = 0.0):

    def callback_func():
        sfx.bufferedOneShotSFX('sfx/Weapons/weapon_change.xml', entity.model)

    if delay:
        BigWorld.callback(delay, callback_func)
    else:
        callback_func()


def JammEffect(entity, delay = 0.0):

    def callback_func():
        pass

    if delay:
        BigWorld.callback(delay, callback_func)
    else:
        callback_func()


def UnJammEffect(entity, delay = 0.0):

    def callback_func():
        pass

    if delay:
        BigWorld.callback(delay, callback_func)
    else:
        callback_func()


def ItemModificationEffect(entity, delay = 0.0):

    def callback_func():
        pass

    if delay:
        BigWorld.callback(delay, callback_func)
    else:
        callback_func()


def AddPixieToEntity(entity, particle_name, node = None, callBackFn = None):

    def onLoadLensFlare(ps):
        node.attach(ps)
        ps.force()
        if callBackFn:
            callBackFn(ps)

    if node == None:
        node = entity.model.root
    onLoadLensFlare(Pixie.create(particle_name))
    return
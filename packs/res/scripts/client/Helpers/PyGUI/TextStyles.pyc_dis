# Embedded file name: scripts/client/Helpers/PyGUI/TextStyles.py
import BigWorld, GUI, Math, ResMgr
from bwdebug import ERROR_MSG
styles = {'Heading': ('ruRU_calibri_default.font', (255, 255, 255, 255)),
 'Label': ('ruRU_calibri_default.font', (255, 255, 255, 255)),
 'ButtonNormal': ('ruRU_calibri_default.font', (175, 166, 112, 255)),
 'ButtonHover': ('ruRU_calibri_default.font', (175, 166, 112, 255)),
 'ButtonPressed': ('ruRU_calibri_default.font', (175, 166, 112, 255)),
 'ButtonActive': ('ruRU_calibri_default.font', (175, 166, 112, 255)),
 'ButtonDisabled': ('ruRU_calibri_default.font', (64, 64, 64, 255)),
 'hlinkNormal': ('ruRU_calibri_default.font', (1, 46, 160, 255)),
 'hlinkHover': ('ruRU_calibri_default.font', (157, 162, 255, 255)),
 'hlinkPressed': ('ruRU_calibri_default.font', (54, 0, 255, 255)),
 'hlinkDisabled': ('ruRU_calibri_default.font', (115, 155, 115, 255)),
 'DDL_Normal': ('ruRU_calibri_default.font', (175, 166, 112, 255)),
 'DDL_Hover': ('ruRU_calibri_default.font', (175, 166, 112, 255)),
 'DDL_Pressed': ('ruRU_calibri_default.font', (175, 166, 112, 255)),
 'DDL_Active': ('ruRU_calibri_default.font', (175, 166, 112, 255)),
 'DDL_Disabled': ('ruRU_calibri_default.font', (64, 64, 64, 255)),
 'listElement_Normal': ('ruRU_calibri_default.font', (175, 166, 112, 255)),
 'listElement_Active': ('ruRU_calibri_default.font', (85, 85, 85, 255)),
 'ButtonNormal_12': ('ruRU_Cyrvetica_Extra_12i.font', (175, 166, 112, 255)),
 'ButtonHover_12': ('ruRU_Cyrvetica_Extra_12i.font', (175, 166, 112, 255)),
 'ButtonPressed_12': ('ruRU_Cyrvetica_Extra_12i.font', (175, 166, 112, 255)),
 'ButtonActive_12': ('ruRU_Cyrvetica_Extra_12i.font', (175, 166, 112, 255)),
 'ButtonDisabled_12': ('ruRU_Cyrvetica_Extra_12i.font', (64, 64, 64, 255)),
 'CharTabNormal': ('ruRU_Cyrvetica_Extra_12i.font', (175, 166, 112, 255)),
 'CharTabHover': ('ruRU_Cyrvetica_Extra_12i.font', (249, 233, 137, 255)),
 'CharTabPressed': ('ruRU_Cyrvetica_Extra_12i.font', (249, 233, 137, 255)),
 'CharTabDisabled': ('ruRU_Cyrvetica_Extra_12i.font', (85, 85, 85, 255)),
 'MainMenuNormal': ('ruRU_Verdana_21.font', (140, 141, 126, 255)),
 'MainMenuHover': ('ruRU_Verdana_21.font', (215, 220, 215, 255)),
 'MainMenuPressed': ('ruRU_Verdana_21.font', (100, 100, 100, 255)),
 'MainMenuDisabled': ('ruRU_Verdana_21.font', (64, 64, 64, 255)),
 'MainMenuBtnNormal': ('ruRU_calibri_default.font', (140, 141, 126, 255)),
 'MainMenuBtnHover': ('ruRU_calibri_default.font', (188, 189, 181, 255)),
 'MainMenuBtnPressed': ('ruRU_calibri_default.font', (188, 189, 181, 255)),
 'MainMenuBtnDisabled': ('ruRU_calibri_default.font', (64, 64, 64, 255)),
 'MainMenuBtnNormalGold': ('ruRU_Verdana_21.font', (222, 185, 120, 255)),
 'MainMenuHoverGold': ('ruRU_Verdana_21.font', (163, 117, 39, 255))}
fontAliases = {}

def setStyle(component, styleName):
    if styles.has_key(styleName):
        style = styles[styleName]
        component.font = fontAliases.get(style[0], style[0])
        component.colour = style[1]
    else:
        ERROR_MSG("No style named '%s'." % (styleName,))
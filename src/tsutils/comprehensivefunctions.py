#-------------------------------------------------------------------------------
# Name:        TagSelector                  # Author:      DarkTrick
# Copyright:   (c) DarkTrick since 2016     # Licence:     CC-BY
#-------------------------------------------------------------------------------

class ComprehensiveFunctions: # comprehensive = uebergreifend
    @staticmethod
    def addTags(EditorObject, strTags):
        tags = EditorObject.tags

        tags.setText(tags.text() + " " + strTags)
        EditorObject.saveTags()
        #TODO: send signal "lostfocus" would be cleaner! (aqt/editor.py:629)

    # --------------------------------------------------------------------
    @staticmethod
    def _removeSpaceSeperatedStrFromStr(strCurrentTags, strTagsToRemvoe):
        # 1. convert string to array
        # 2. manipulate array
        # 3. convert array to string

        splitDelimiter = " " # TODO: should handle other white-spaces!
        arrayCurrentTags = strCurrentTags.split(splitDelimiter)
        arrayNewTags = strCurrentTags.split(splitDelimiter)
        arrayToRemove = strTagsToRemvoe.split(splitDelimiter)

        # Remove all tags specified - Bugfix: CASE INSENSITIVE
        for oneTagToRemove in arrayToRemove:
            for currentTag in arrayCurrentTags:
                if(currentTag.lower() == oneTagToRemove.lower()):
                    arrayNewTags.remove(currentTag)

        return " ".join(arrayNewTags)

    # ---------------------------------------------------------------------
    @staticmethod
    def removeTags(EditorObject, strTagsToRemove):
        currentTags = EditorObject.tags.text()
        newTags = ComprehensiveFunctions._removeSpaceSeperatedStrFromStr(
            currentTags, strTagsToRemove)
        EditorObject.tags.setText(newTags)

        # do we need this?
        # EditorObject.saveTags()
        #TODO: send signal "lostfocus" would be cleaner! (aqt/editor.py:629)
        pass

    # ---------------------------------------------------------------------
    @staticmethod
    def replaceAllWhitespaces(sourceString, replacerString):
        ret = sourceString
        ret = ret.replace(u'\u00A0',replacerString)
        ret = ret.replace("\t",replacerString)
        ret = ret.replace(" ",replacerString)
        ret = ret.replace(u'\u3000',replacerString)
        return ret
        pass
    # --------------------------------------------------------------------


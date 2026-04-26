/*
 * Allianz Income and Growth Factsheet — InDesign Style Setup Script
 *
 * Run this script in InDesign to auto-create all colour swatches,
 * paragraph styles, character styles, table styles, cell styles,
 * and object styles needed for the factsheet XML import.
 *
 * HOW TO RUN:
 *   1. Open InDesign
 *   2. Create or open your 6-page US Letter document
 *   3. File > Scripts > run this .jsx file
 *      (or Window > Utilities > Scripts, then double-click)
 *   4. All styles will be created. Then import the .xmp file.
 *
 * Safe to re-run: existing styles with matching names are skipped.
 */

(function () {
    var doc;
    if (app.documents.length === 0) {
        doc = app.documents.add();
        doc.documentPreferences.pageWidth = "8.5in";
        doc.documentPreferences.pageHeight = "11in";
        doc.documentPreferences.facingPages = false;
        while (doc.pages.length < 6) {
            doc.pages.add();
        }
        doc.marginPreferences.top = "0.5in";
        doc.marginPreferences.bottom = "0.55in";
        doc.marginPreferences.left = "0.6in";
        doc.marginPreferences.right = "0.6in";
    } else {
        doc = app.activeDocument;
    }

    // ================================================================
    // HELPER: get or create a colour swatch (RGB mode for screen/digital)
    // ================================================================
    function swatch(name, r, g, b) {
        try {
            return doc.colors.itemByName(name);
        } catch (e) {}
        if (doc.colors.itemByName(name).isValid) {
            return doc.colors.itemByName(name);
        }
        var c = doc.colors.add();
        c.name = name;
        c.model = ColorModel.PROCESS;
        c.space = ColorSpace.RGB;
        c.colorValue = [r, g, b];
        return c;
    }

    // ================================================================
    // COLOUR SWATCHES
    // ================================================================
    var navy900  = swatch("Navy 900",   7,  25,  53);
    var navy800  = swatch("Navy 800",  10,  35,  71);
    var navy700  = swatch("Navy 700",  14,  48,  94);
    var blue600  = swatch("Blue 600",   3,  66, 228);
    var blue500  = swatch("Blue 500",  26, 109, 255);
    var blue100  = swatch("Blue 100", 232, 238, 251);
    var blue50   = swatch("Blue 50",  240, 244, 253);
    var slate600 = swatch("Slate 600", 58,  64,  81);
    var slate500 = swatch("Slate 500", 74,  82, 103);
    var slate400 = swatch("Slate 400",107, 114, 128);
    var slate300 = swatch("Slate 300",156, 163, 175);
    var gray200  = swatch("Gray 200", 229, 231, 235);
    var gray100  = swatch("Gray 100", 243, 244, 246);
    var gray50   = swatch("Gray 50",  249, 250, 251);
    var green700 = swatch("Green 700", 21, 128,  61);
    var green600 = swatch("Green 600", 22, 163,  74);
    var green100 = swatch("Green 100",220, 252, 231);
    var green50  = swatch("Green 50", 240, 253, 244);
    var red700   = swatch("Red 700",  185,  28,  28);
    var red600   = swatch("Red 600",  220,  38,  38);
    var red100   = swatch("Red 100",  254, 226, 226);
    var amber600 = swatch("Amber 600",217, 119,   6);
    var amber100 = swatch("Amber 100",254, 243, 199);
    var amber50  = swatch("Amber 50", 255, 251, 235);
    var indigo   = swatch("Indigo",    99, 102, 241);

    // ================================================================
    // HELPER: get or create paragraph style
    // ================================================================
    function pstyle(name, props) {
        var s;
        try {
            s = doc.paragraphStyles.itemByName(name);
            if (s.isValid) return s;
        } catch (e) {}
        s = doc.paragraphStyles.add({ name: name });
        applyProps(s, props);
        return s;
    }

    // ================================================================
    // HELPER: get or create character style
    // ================================================================
    function cstyle(name, props) {
        var s;
        try {
            s = doc.characterStyles.itemByName(name);
            if (s.isValid) return s;
        } catch (e) {}
        s = doc.characterStyles.add({ name: name });
        applyProps(s, props);
        return s;
    }

    // ================================================================
    // HELPER: apply properties safely
    // ================================================================
    function applyProps(style, props) {
        for (var key in props) {
            if (props.hasOwnProperty(key)) {
                try {
                    style[key] = props[key];
                } catch (e) {
                    // Some properties may not apply in all contexts
                }
            }
        }
    }

    // ================================================================
    // FONT HELPERS
    // ================================================================
    var fontInter = "Inter";
    var fontFallback = "Helvetica Neue";

    function findFont(family, styleName) {
        try {
            var f = app.fonts.itemByName(family + "\t" + styleName);
            if (f.isValid) return f;
        } catch (e) {}
        try {
            var f2 = app.fonts.itemByName(fontFallback + "\t" + styleName);
            if (f2.isValid) return f2;
        } catch (e2) {}
        return undefined;
    }

    var fRegular    = findFont(fontInter, "Regular");
    var fMedium     = findFont(fontInter, "Medium");
    var fSemiBold   = findFont(fontInter, "SemiBold") || findFont(fontInter, "Semi Bold");
    var fBold       = findFont(fontInter, "Bold");
    var fExtraBold  = findFont(fontInter, "ExtraBold") || findFont(fontInter, "Extra Bold");

    // ================================================================
    // PARAGRAPH STYLES
    // ================================================================

    // -- Headers & Titles --
    pstyle("Fund Title", {
        appliedFont: fExtraBold || fBold,
        pointSize: 16,
        leading: 18,
        fillColor: "Paper",
        spaceAfter: "2pt",
        tracking: -30
    });

    pstyle("Fund Subtitle", {
        appliedFont: fRegular,
        pointSize: 8,
        leading: 10,
        fillColor: "Paper",
    });

    pstyle("Report Date", {
        appliedFont: fSemiBold || fBold,
        pointSize: 8,
        leading: 10,
        fillColor: "Paper",
        justification: Justification.RIGHT_ALIGN
    });

    pstyle("Badge", {
        appliedFont: fSemiBold || fBold,
        pointSize: 7,
        leading: 9,
        fillColor: "Paper",
    });

    // -- Section Headings --
    pstyle("Section Heading", {
        appliedFont: fBold,
        pointSize: 10,
        leading: 13,
        fillColor: navy900,
        spaceBefore: "8pt",
        spaceAfter: "5pt"
    });

    pstyle("Section Description", {
        appliedFont: fRegular,
        pointSize: 7,
        leading: 9,
        fillColor: slate400,
    });

    pstyle("Subsection Heading", {
        appliedFont: fBold,
        pointSize: 8,
        leading: 10,
        fillColor: navy900,
        spaceBefore: "6pt",
        spaceAfter: "4pt"
    });

    // -- Commentary --
    pstyle("Commentary Body", {
        appliedFont: fRegular,
        pointSize: 8,
        leading: "12.4pt",
        fillColor: slate600,
        spaceAfter: "7pt"
    });

    pstyle("Disclaimer", {
        appliedFont: fRegular,
        pointSize: 6.5,
        leading: 8,
        fillColor: amber600,
        justification: Justification.CENTER_ALIGN
    });

    // -- Metric Cards --
    pstyle("Metric Label", {
        appliedFont: fBold,
        pointSize: 5.5,
        leading: 7,
        fillColor: slate400,
        justification: Justification.CENTER_ALIGN,
        capitalization: Capitalization.ALL_CAPS,
        tracking: 80
    });

    pstyle("Metric Value Positive", {
        appliedFont: fExtraBold || fBold,
        pointSize: 14,
        leading: "15.4pt",
        fillColor: green600,
        justification: Justification.CENTER_ALIGN,
        tracking: -20
    });

    pstyle("Metric Value Negative", {
        appliedFont: fExtraBold || fBold,
        pointSize: 14,
        leading: "15.4pt",
        fillColor: red600,
        justification: Justification.CENTER_ALIGN,
        tracking: -20
    });

    pstyle("Metric Value Neutral", {
        appliedFont: fExtraBold || fBold,
        pointSize: 14,
        leading: "15.4pt",
        fillColor: navy900,
        justification: Justification.CENTER_ALIGN,
        tracking: -20
    });

    pstyle("Metric Value Amber", {
        appliedFont: fExtraBold || fBold,
        pointSize: 14,
        leading: "15.4pt",
        fillColor: amber600,
        justification: Justification.CENTER_ALIGN,
        tracking: -20
    });

    pstyle("Metric Context", {
        appliedFont: fRegular,
        pointSize: 6,
        leading: 8,
        fillColor: slate400,
        justification: Justification.CENTER_ALIGN
    });

    // -- Investor Profile --
    pstyle("Profile Label", {
        appliedFont: fBold,
        pointSize: 5.5,
        leading: 7,
        fillColor: blue600,
        capitalization: Capitalization.ALL_CAPS,
        tracking: 60
    });

    pstyle("Profile Value", {
        appliedFont: fSemiBold || fBold,
        pointSize: 8,
        leading: 10,
        fillColor: navy900,
    });

    // -- Tables --
    pstyle("Table Caption", {
        appliedFont: fBold,
        pointSize: 8,
        leading: 10,
        fillColor: navy900,
        spaceAfter: "5pt"
    });

    pstyle("Table Header", {
        appliedFont: fSemiBold || fBold,
        pointSize: 6,
        leading: 8,
        fillColor: slate500,
        capitalization: Capitalization.ALL_CAPS,
        tracking: 40
    });

    pstyle("Table Header Right", {
        appliedFont: fSemiBold || fBold,
        pointSize: 6,
        leading: 8,
        fillColor: slate500,
        capitalization: Capitalization.ALL_CAPS,
        tracking: 40,
        justification: Justification.RIGHT_ALIGN
    });

    pstyle("Table Header Dark", {
        appliedFont: fSemiBold || fBold,
        pointSize: 6,
        leading: 8,
        fillColor: "Paper",
        capitalization: Capitalization.ALL_CAPS,
        tracking: 40
    });

    pstyle("Table Header Dark Right", {
        appliedFont: fSemiBold || fBold,
        pointSize: 6,
        leading: 8,
        fillColor: "Paper",
        capitalization: Capitalization.ALL_CAPS,
        tracking: 40,
        justification: Justification.RIGHT_ALIGN
    });

    pstyle("Table Cell", {
        appliedFont: fRegular,
        pointSize: 7.5,
        leading: 10,
        fillColor: slate600,
    });

    pstyle("Table Cell Right", {
        appliedFont: fRegular,
        pointSize: 7.5,
        leading: 10,
        fillColor: slate600,
        justification: Justification.RIGHT_ALIGN
    });

    pstyle("Table Cell Label", {
        appliedFont: fSemiBold || fBold,
        pointSize: 7.5,
        leading: 10,
        fillColor: navy900,
    });

    pstyle("Table Cell Label Bold", {
        appliedFont: fBold,
        pointSize: 7.5,
        leading: 10,
        fillColor: navy900,
    });

    pstyle("Table Cell Positive", {
        appliedFont: fSemiBold || fBold,
        pointSize: 7.5,
        leading: 10,
        fillColor: green600,
        justification: Justification.RIGHT_ALIGN
    });

    pstyle("Table Cell Negative", {
        appliedFont: fSemiBold || fBold,
        pointSize: 7.5,
        leading: 10,
        fillColor: red600,
        justification: Justification.RIGHT_ALIGN
    });

    pstyle("Table Cell Amber", {
        appliedFont: fSemiBold || fBold,
        pointSize: 7.5,
        leading: 10,
        fillColor: amber600,
    });

    pstyle("Table Footnote", {
        appliedFont: fRegular,
        pointSize: 5.5,
        leading: 7,
        fillColor: slate400,
        spaceBefore: "5pt"
    });

    // -- Callouts --
    pstyle("Callout Blue", {
        appliedFont: fRegular,
        pointSize: 7.5,
        leading: "11.25pt",
        fillColor: navy900,
    });

    pstyle("Callout Green", {
        appliedFont: fRegular,
        pointSize: 7.5,
        leading: "11.25pt",
        fillColor: green700,
    });

    pstyle("Callout Amber", {
        appliedFont: fRegular,
        pointSize: 7.5,
        leading: "11.25pt",
        fillColor: slate600,
    });

    // -- Outlook --
    pstyle("Outlook Indicator", {
        appliedFont: fRegular,
        pointSize: 10,
        leading: 12,
        fillColor: navy900,
        justification: Justification.CENTER_ALIGN
    });

    pstyle("Outlook Label", {
        appliedFont: fSemiBold || fBold,
        pointSize: 5.5,
        leading: 7,
        fillColor: slate400,
        justification: Justification.CENTER_ALIGN,
        capitalization: Capitalization.ALL_CAPS,
        tracking: 40
    });

    pstyle("Outlook Value Positive", {
        appliedFont: fBold,
        pointSize: 7,
        leading: 9,
        fillColor: green600,
        justification: Justification.CENTER_ALIGN
    });

    pstyle("Outlook Value Neutral", {
        appliedFont: fBold,
        pointSize: 7,
        leading: 9,
        fillColor: navy900,
        justification: Justification.CENTER_ALIGN
    });

    pstyle("Outlook Value Amber", {
        appliedFont: fBold,
        pointSize: 7,
        leading: 9,
        fillColor: amber600,
        justification: Justification.CENTER_ALIGN
    });

    // -- Lists (Opportunities & Risks) --
    pstyle("List Heading Green", {
        appliedFont: fBold,
        pointSize: 8,
        leading: 10,
        fillColor: green700,
    });

    pstyle("List Heading Red", {
        appliedFont: fBold,
        pointSize: 8,
        leading: 10,
        fillColor: red600,
    });

    pstyle("Opportunity Item", {
        appliedFont: fRegular,
        pointSize: 7,
        leading: "9.8pt",
        fillColor: slate600,
        leftIndent: "10pt",
        firstLineIndent: "-10pt",
        bulletsAndNumberingListType: ListType.BULLET_LIST,
    });

    pstyle("Risk Item", {
        appliedFont: fRegular,
        pointSize: 7,
        leading: "9.8pt",
        fillColor: slate600,
        leftIndent: "10pt",
        firstLineIndent: "-10pt",
        bulletsAndNumberingListType: ListType.BULLET_LIST,
    });

    // -- ESG --
    pstyle("ESG Badge", {
        appliedFont: fBold,
        pointSize: 6,
        leading: 8,
        fillColor: green700,
        capitalization: Capitalization.ALL_CAPS,
        tracking: 40
    });

    pstyle("ESG Body", {
        appliedFont: fRegular,
        pointSize: 7.5,
        leading: 12,
        fillColor: slate600,
        spaceAfter: "6pt"
    });

    pstyle("ESG Link", {
        appliedFont: fRegular,
        pointSize: 7,
        leading: "10.5pt",
        fillColor: slate500,
    });

    // -- Team --
    pstyle("Team Initials", {
        appliedFont: fBold,
        pointSize: 6,
        leading: 8,
        fillColor: "Paper",
        justification: Justification.CENTER_ALIGN
    });

    pstyle("Team Name", {
        appliedFont: fSemiBold || fBold,
        pointSize: 7.5,
        leading: 10,
        fillColor: navy900,
    });

    pstyle("Team Role", {
        appliedFont: fRegular,
        pointSize: 6,
        leading: 8,
        fillColor: slate400,
    });

    // -- Author --
    pstyle("Author Initials", {
        appliedFont: fBold,
        pointSize: 6,
        leading: 8,
        fillColor: "Paper",
        justification: Justification.CENTER_ALIGN
    });

    pstyle("Author Name", {
        appliedFont: fSemiBold || fBold,
        pointSize: 7,
        leading: 9,
        fillColor: navy900,
    });

    pstyle("Author Role", {
        appliedFont: fRegular,
        pointSize: 6,
        leading: 8,
        fillColor: slate400,
    });

    // -- Fund Info --
    pstyle("Info Group Heading", {
        appliedFont: fBold,
        pointSize: 8,
        leading: 10,
        fillColor: navy900,
        spaceAfter: "4pt"
    });

    pstyle("Info Label", {
        appliedFont: fRegular,
        pointSize: 7,
        leading: 9,
        fillColor: slate400,
    });

    pstyle("Info Value", {
        appliedFont: fSemiBold || fBold,
        pointSize: 7,
        leading: 9,
        fillColor: navy900,
        justification: Justification.RIGHT_ALIGN
    });

    // -- CTA --
    pstyle("CTA Heading", {
        appliedFont: fBold,
        pointSize: 9,
        leading: 11,
        fillColor: "Paper",
    });

    pstyle("CTA Body", {
        appliedFont: fRegular,
        pointSize: 7,
        leading: 9,
        fillColor: "Paper",
    });

    pstyle("CTA Link", {
        appliedFont: fSemiBold || fBold,
        pointSize: 7,
        leading: 9,
        fillColor: navy900,
    });

    pstyle("CTA Link Secondary", {
        appliedFont: fSemiBold || fBold,
        pointSize: 7,
        leading: 9,
        fillColor: "Paper",
    });

    // -- Footnotes & Legal --
    pstyle("Footnote", {
        appliedFont: fRegular,
        pointSize: 6,
        leading: 9,
        fillColor: slate400,
        leftIndent: "12pt",
        firstLineIndent: "-12pt",
        spaceAfter: "3pt"
    });

    pstyle("Attribution", {
        appliedFont: fRegular,
        pointSize: 6,
        leading: 9,
        fillColor: slate400,
        spaceBefore: "4pt"
    });

    pstyle("Legal Heading", {
        appliedFont: fBold,
        pointSize: 6.5,
        leading: "9.75pt",
        fillColor: slate600,
    });

    pstyle("Legal Body", {
        appliedFont: fRegular,
        pointSize: 6.5,
        leading: "10.4pt",
        fillColor: slate400,
        spaceAfter: "5pt"
    });

    pstyle("Legal Signoff", {
        appliedFont: fSemiBold || fBold,
        pointSize: 7,
        leading: 9,
        fillColor: slate600,
        spaceBefore: "10pt"
    });

    pstyle("Risk Note", {
        appliedFont: fRegular,
        pointSize: 6,
        leading: 8,
        fillColor: slate400,
    });

    // -- Page Footer --
    pstyle("Page Footer Brand", {
        appliedFont: fSemiBold || fBold,
        pointSize: 6.5,
        leading: 8,
        fillColor: slate300,
        tracking: 40
    });

    pstyle("Page Footer Number", {
        appliedFont: fMedium || fRegular,
        pointSize: 7,
        leading: 9,
        fillColor: slate400,
        justification: Justification.RIGHT_ALIGN
    });

    // ================================================================
    // CHARACTER STYLES
    // ================================================================
    cstyle("Commentary Label", {
        appliedFont: fBold,
        fillColor: navy900,
    });

    cstyle("Callout Heading", {
        appliedFont: fBold,
    });

    // ================================================================
    // TABLE STYLES & CELL STYLES
    // ================================================================

    // Cell styles
    function cellStyle(name, props) {
        var s;
        try {
            s = doc.cellStyles.itemByName(name);
            if (s.isValid) return s;
        } catch (e) {}
        s = doc.cellStyles.add({ name: name });
        applyProps(s, props);
        return s;
    }

    var csHeader = cellStyle("Header Cell", {
        topInset: "3.5pt",
        bottomInset: "3.5pt",
        leftInset: "6pt",
        rightInset: "6pt",
    });

    var csBody = cellStyle("Body Cell", {
        topInset: "3.5pt",
        bottomInset: "3.5pt",
        leftInset: "6pt",
        rightInset: "6pt",
    });

    var csHighlight = cellStyle("Highlight Cell", {
        topInset: "3.5pt",
        bottomInset: "3.5pt",
        leftInset: "6pt",
        rightInset: "6pt",
    });

    // Table styles
    function tableStyle(name, props) {
        var s;
        try {
            s = doc.tableStyles.itemByName(name);
            if (s.isValid) return s;
        } catch (e) {}
        s = doc.tableStyles.add({ name: name });
        applyProps(s, props);
        return s;
    }

    tableStyle("Data Table", {
        headerRegionCellStyle: csHeader,
        bodyRegionCellStyle: csBody,
        spaceBefore: "6pt",
        spaceAfter: "6pt",
    });

    tableStyle("Dark Header Table", {
        headerRegionCellStyle: csHeader,
        bodyRegionCellStyle: csBody,
        spaceBefore: "6pt",
        spaceAfter: "6pt",
    });

    tableStyle("Peer Table", {
        headerRegionCellStyle: csHeader,
        bodyRegionCellStyle: csBody,
        spaceBefore: "6pt",
        spaceAfter: "6pt",
    });

    // ================================================================
    // OBJECT STYLES
    // ================================================================
    function objStyle(name, props) {
        var s;
        try {
            s = doc.objectStyles.itemByName(name);
            if (s.isValid) return s;
        } catch (e) {}
        s = doc.objectStyles.add({ name: name });
        applyProps(s, props);
        return s;
    }

    objStyle("Card Frame", {
        fillColor: "Paper",
        strokeColor: gray200,
        strokeWeight: "0.5pt",
        enableStroke: true,
    });

    objStyle("Callout Blue Frame", {
        fillColor: blue50,
        strokeColor: blue600,
        strokeWeight: "3pt",
        enableStroke: true,
    });

    objStyle("Callout Green Frame", {
        fillColor: green50,
        strokeColor: green600,
        strokeWeight: "3pt",
        enableStroke: true,
    });

    objStyle("Callout Amber Frame", {
        fillColor: amber50,
        strokeColor: amber600,
        strokeWeight: "3pt",
        enableStroke: true,
    });

    objStyle("ESG Card Frame", {
        fillColor: green50,
        strokeColor: green100,
        strokeWeight: "0.5pt",
        enableStroke: true,
    });

    objStyle("CTA Strip Frame", {
        fillColor: navy900,
        enableStroke: false,
    });

    objStyle("Team Card Frame", {
        fillColor: gray50,
        strokeColor: gray200,
        strokeWeight: "0.5pt",
        enableStroke: true,
    });

    objStyle("Header Band Frame", {
        fillColor: navy900,
        enableStroke: false,
    });

    // ================================================================
    // DONE
    // ================================================================
    var pCount = 0, cCount = 0, tCount = 0, oCount = 0, swCount = 0;
    pCount = doc.paragraphStyles.length - 2; // minus [No Paragraph Style] and [Basic Paragraph]
    cCount = doc.characterStyles.length - 1; // minus [None]
    tCount = doc.tableStyles.length - 1;     // minus [No Table Style]
    oCount = doc.objectStyles.length - 2;    // minus [None] and [Basic Graphics Frame]
    swCount = doc.colors.length;

    alert(
        "Factsheet styles created successfully!\n\n" +
        "Colour Swatches: " + swCount + "\n" +
        "Paragraph Styles: " + pCount + "\n" +
        "Character Styles: " + cCount + "\n" +
        "Table Styles: " + tCount + "\n" +
        "Object Styles: " + oCount + "\n\n" +
        "Next steps:\n" +
        "1. File > Import XML > select allianz_factsheet_indesign.xmp\n" +
        "2. Tags panel > Map Tags to Styles > Map By Name\n" +
        "3. Drag <factsheet> into your text frame\n" +
        "4. Export PDF with 'Create Tagged PDF' enabled"
    );

})();

/* *
 *
 *  (c) 2009-2024 Highsoft AS
 *
 *  License: www.highcharts.com/license
 *
 *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
 *
 *  Authors:
 *  - Dawid Dragula
 *  - Sebastian Bochan
 *
 * */
'use strict';
/* *
 *
 *  Imports
 *
 * */
/* *
 *
 *  Namespace
 *
 * */
/**
 * Global DataGrid namespace.
 *
 * @namespace DataGrid
 */
var Globals;
(function (Globals) {
    /* *
     *
     *  Declarations
     *
     * */
    /* *
     *
     *  Constants
     *
     * */
    Globals.classNamePrefix = 'highcharts-datagrid-';
    Globals.classNames = {
        container: Globals.classNamePrefix + 'container',
        tableElement: Globals.classNamePrefix + 'table',
        captionElement: Globals.classNamePrefix + 'caption',
        theadElement: Globals.classNamePrefix + 'thead',
        tbodyElement: Globals.classNamePrefix + 'tbody',
        rowElement: Globals.classNamePrefix + 'row',
        rowOdd: Globals.classNamePrefix + 'row-odd',
        hoveredRow: Globals.classNamePrefix + 'hovered-row',
        columnElement: Globals.classNamePrefix + 'column',
        hoveredCell: Globals.classNamePrefix + 'hovered-cell',
        hoveredColumn: Globals.classNamePrefix + 'hovered-column',
        editedCell: Globals.classNamePrefix + 'edited-cell',
        rowsContentNowrap: Globals.classNamePrefix + 'rows-content-nowrap',
        headerCell: Globals.classNamePrefix + 'header-cell',
        headerCellContent: Globals.classNamePrefix + 'header-cell-content',
        headerCellResized: Globals.classNamePrefix + 'header-cell-resized',
        headerRow: Globals.classNamePrefix + 'head-row-content',
        noData: Globals.classNamePrefix + 'no-data',
        columnFirst: Globals.classNamePrefix + 'column-first',
        columnSortable: Globals.classNamePrefix + 'column-sortable',
        columnSortedAsc: Globals.classNamePrefix + 'column-sorted-asc',
        columnSortedDesc: Globals.classNamePrefix + 'column-sorted-desc',
        resizerHandles: Globals.classNamePrefix + 'column-resizer',
        resizedColumn: Globals.classNamePrefix + 'column-resized',
        creditsContainer: Globals.classNamePrefix + 'credits-container',
        creditsText: Globals.classNamePrefix + 'credits'
    };
    Globals.win = window;
    Globals.userAgent = (Globals.win.navigator && Globals.win.navigator.userAgent) || '';
    Globals.isChrome = Globals.userAgent.indexOf('Chrome') !== -1;
    Globals.isSafari = !Globals.isChrome && Globals.userAgent.indexOf('Safari') !== -1;
})(Globals || (Globals = {}));
/* *
 *
 *  Default Export
 *
 * */
export default Globals;

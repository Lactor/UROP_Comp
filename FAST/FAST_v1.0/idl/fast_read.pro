;......................................................................
;description:
; Reads unformatted data file and header
;
;parameters:
; input    input_file  name input file
;          format      'flt','str','dbl' or 'int'
; keyword  comment
;          header
; return   data        data array
;......................................................................

FUNCTION fast_read, input_file, format, comment=comment, header=header

header = ''
if not KEYWORD_SET(comment) then comment='#'

CASE format OF
    'str': type = 7
    'int': type = 3 ; long 
    'flt': type = 4 
    'dbl': type = 5
    ELSE: type = 4
ENDCASE

; read entire file in string buffer
n = file_lines(input_file) ;number of lines in file
lines = strarr(n)  ; allocates an array of strings
openr, lun, input_file, /get_lun
readf, lun, lines ; reads lines to array
close, lun & free_lun, lun

; locate comment and data lines from first character
first_char = strmid(lines,0,1) ;array of first charactes
ihdr = where(first_char eq comment, nhdr, complement=idata, ncomplement=ndata) ;places where it is a comment (header)
if ndata eq 0 then message, 'ERROR: '+fname+' contains no data' ;has to contain data
ncol = n_elements(strsplit(lines[idata[0]])) ;splits the lines with data

; parse header
if nhdr gt 0 then begin
  h = strmid(lines[ihdr],1)   ; strip comment symbol  lines that start with comment
  for i=0,n_elements(h)-1 do begin
      head_line = strsplit(h[i],/extract)  ; split into substrings
      nhcol     = n_elements(head_line) ;number of columns
      if nhcol eq ncol then begin ; number of header tags must equal the number of columns of data
          if n_elements(header) eq 0 or n_elements(header) eq 1 then $
            header = head_line else header = [[header],[head_line]] ;create the header or add info
      endif
  endfor
endif

; split lines into words, cast to correct type, and fill array
; 45% of the total time is spent in strsplit, 45% in casting of 
; the data type (fix)
data = make_array(ncol, ndata, type=type) ; Make array of size and correct type
for i=0L, ndata-1 do begin
    if n_elements(strsplit(lines[idata[i]],/extract)) ne ncol then begin
       print,'ERROR: when reading '+input_file
       print,'       number of columns is not constant throughout file'
       exit
    endif
    data[*,i] = fix( strsplit(lines[idata[i]],/extract), type=type) ; for each line of data add to the data file
endfor
 
return, data ; return data

END

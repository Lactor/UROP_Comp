function fast_no_filters,CATALOG

comment = '#'
l_com   = strlen(comment)
line    = ''
w_head  = 0
w_data  = 0

;...determine the number of data columns
OPENR, unit, CATALOG+'.cat', /GET_LUN
; opens file (unit defines the pointer to the file)
while w_data eq 0 do begin
    READF, unit, line
    col   = strsplit(line, /extract)
    if strmid(col(0),0,l_com) ne comment then begin
        n_col  = n_elements(col)
        w_data = 1
     endif
     ;obtains the number of columns and stores on n_col
endwhile
CLOSE, unit
FREE_LUN, unit
;Free memory


;...read header with same number of columns as the data
OPENR, unit, CATALOG+'.cat', /GET_LUN
while w_head eq 0 do begin
    READF, unit, line
    col = strsplit(line, /extract)
    ;seperate into substrings the line of text
    if strmid(col(0),0,l_com) eq comment and n_elements(col) gt 1 $
       ; header starts with a comment
      then begin
        ;...first entry may be attached to '#'
        if col(0) eq comment then tmp_head = col(1:(n_elements(col)-1)) $
        else tmp_head = [strmid(col(0),1),col(1:(n_elements(col)-1))]
        ; if the header starts with # removes it
        if n_elements(tmp_head) eq n_col then begin
            if n_elements(header) eq 0 then header = tmp_head else $
              header = [[header],[tmp_head]]
            ;adds information to the header array
        endif
    endif else begin
        w_head = 1
    endelse
endwhile
CLOSE, unit
FREE_LUN, unit

;...change header file in case CATALOG.TRANSLATE is provided
if FILE_TEST(CATALOG+'.translate') then begin
   readcol,CATALOG+'.translate',tr1,tr2,format='(A,A)',/silent
   for i=0,n_elements(tr1)-1 do begin
      rep_h = where(header eq tr1(i),n_rep_h)
      if n_rep_h eq 1 then begin
         if (size(header))[0] eq 1 then begin
            header(rep_h) = tr2(i) ;if header is one dimension just substitute
         endif else begin
            rep_h2 = array_indices(header,rep_h) ;if header is two dimensional find the two indices and substitute then
            header(rep_h2(0),rep_h2(1)) = tr2(i)
         endelse
      endif
   endfor
endif
;Change the header names by their translations

;...determine filters from the header info
if (size(header))[0] eq 0 then begin
   print,"ERROR: no header found in "+CATALOG
   print,"       Check that number of data columns is the same as header columns"
   exit
endif
if (size(header))[0] eq 1 then n_line_h = 1
if (size(header))[0] eq 2 then n_line_h = (size(header))[2]
header = REFORM(header,(size(header))[1],n_line_h) ; Forces header to be two dimensional
i_line = (array_indices(header,where(strmatch(header,'F*[1234567890]') eq 1)))[1,0] ;Finds the line where the F are found
fl_ind = where(strmatch(header,'F*[1234567890]') eq 1,n_filt) ; finds the positions on line where fl_ind occur
filt   = strmid(header(fl_ind,i_line),1) ; gets the values of the header F index.

return,filt

end



FUNCTION fast_read_filters,FILTERS_RES,lambda,CATALOG=CATALOG,$
                           SPECTRUM=SPECTRUM,no_filt=no_filt


;...read photometric filters
;   RECENT EDIT: added "or Keyowrd_set(no_filt)
if KEYWORD_SET(CATALOG) or KEYWORD_SET(no_filt) then begin ;need to define either the catalogue of the no_filt

   if not KEYWORD_SET(no_filt) then no_filt = fast_no_filters(CATALOG) ;sets no_filt from catalog
   n_filt     = n_elements(no_filt) ;number of F* header tags.

    if not file_test(FILTERS_RES) then begin ;tests the file where the filters should be
        print,"ERROR: defined filter file is not available" & exit
    endif
    READCOL,FILTERS_RES,no,wl,tr,FORMAT='I,F,F',/silent ;Reads 3 columns from the file, no, wl and tr
    st_filt    = where(no eq 1,n_filt_res) ;find places where no = 1 (beggiinng o filters)
    en_filt    = [st_filt(1:n_filt_res-1)-1,n_elements(no)-1]  ; array of the ends of filters
    nel_filt   = en_filt-st_filt+1 ; arrays of length of filters
    lambda     = fltarr(n_elements(no_filt)) ;  creates an array of floats with size equal to the number o no_filt
    c_no_filt  = no_filt-1  ;removes one from each entry of no_filt

    for i=0,n_filt-1 do begin
        tmp_filt = [[REPLICATE(i,nel_filt(c_no_filt(i)))],$
                    [wl(st_filt(c_no_filt(i)):en_filt(c_no_filt(i)))],$
                    [tr(st_filt(c_no_filt(i)):en_filt(c_no_filt(i)))],$
                    [REPLICATE(1,nel_filt(c_no_filt(i)))]] ;photo code  Creates 2 dimensional array where the second dimention has 4 
                                ;row entries, the first is a row of
                                ;the filter number, second and third
                                ;are the entries from file and fourth
                                ;is 1. Every column has size equal to
                                ;the size of filter.
        if i eq 0 then begin
            filters = tmp_filt
        endif else begin
            filters = [filters,tmp_filt] ; adds the tmp_filter to an array of filters, second dimension is still 4!!!
        endelse
        lambda(i) = TOTAL(tmp_filt(*,1)*tmp_filt(*,1)*tmp_filt(*,2)) / $
          TOTAL(tmp_filt(*,1)*tmp_filt(*,2)) ; multiplies the data rows and adds them
    endfor
    filters = TRANSPOSE(TEMPORARY(filters),[1,0]) ;transposes the two coordinates
endif 

if n_elements(n_filt) eq 0 then n_filt  = 0
    
;...read spectroscopic binning info (only if spectrum is defined)
if KEYWORD_SET(SPECTRUM) then begin
    spec        = FAST_READ(SPECTRUM+'.spec','flt',comment='#') ;returns data in spectrum
    n_spec      = (size(spec))[2] ; number of rows of data of data
    n_bin       = n_elements(UNIQ(spec(0,*))) ; number of different binst
    bins        = fltarr(4,n_spec); creates array of dimension 4xn_spec
    bins(0,*)   = spec(0,*)+n_filt ; sets the firs columm of bin to be the first column of data + the number of filters tags
    bins(1:2,*) = spec(1:2,*) ; sets the data columns equals
    bins(3,*)   = REPLICATE(0,n_spec) ;spectral code  
    if n_elements(filters) eq 0 then filters = bins else $
      filters   = [[temporary(filters)],[bins]] ; adds the spectral information to the bins
    tmp_lam     = fltarr(n_bin) ;defines a temporaty lambda the size of the bins
    for i=0l,n_bin-1 do begin ; for each bin
        bin        = where(spec(0,*) eq i) ;  indexes of the rows of a certain bin i
        tmp_lam(i) = TOTAL(spec(1,bin) * spec(2,bin)) / TOTAL(spec(2,bin)) ; a analogous situation to the previous calculation for filters
                                ;but different (less one spec(1, bin)
    endfor
    if n_filt eq 0 then lambda = tmp_lam else $
      lambda = [TEMPORARY(lambda),tmp_lam] ; adds information of the new calculated values to the lambda such that extends first dimension.
endif

RETURN,filters ;returns lambda but lambda and no_filt are passed by reference.

END



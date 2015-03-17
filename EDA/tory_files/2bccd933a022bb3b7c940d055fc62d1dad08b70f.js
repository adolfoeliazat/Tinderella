if (typeof cmSetClientID == 'function') {
    if (/dev/.test(window.location.hostname) || /stage/.test(window.location.hostname)) cmSetClientID('60033273',false,'testdata.coremetrics.com','nordstrom.com');
	else cmSetClientID('90033273',false,'1901.nordstrom.com','nordstrom.com');
}
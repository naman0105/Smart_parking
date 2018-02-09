import cv2
import time
import saveImage
import numpy as np

##################
DELAY = 0.02
USE_CAM = 1
IS_FOUND = 0

MORPH = 7
CANNY = 250
##################
_width  = 600.0
_height = 420.0
_margin = 0.0
##################

if USE_CAM: video_capture = cv2.VideoCapture(0)

corners = np.array(
	[
		[[  		_margin, _margin 			]],
		[[ 			_margin, _height + _margin  ]],
		[[ _width + _margin, _height + _margin  ]],
		[[ _width + _margin, _margin 			]],
	]
)

pts_dst = np.array( corners, np.float32 )

while True :

	if USE_CAM :
		ret, rgb = video_capture.read()
	else :
		ret = 1
		rgb = cv2.imread( "opencv.jpg", 1 )

	if ( ret ):

		gray = cv2.cvtColor( rgb, cv2.COLOR_BGR2GRAY )

		gray = cv2.bilateralFilter( gray, 1, 10, 120 )

		edges  = cv2.Canny( gray, 10, CANNY )

		kernel = cv2.getStructuringElement( cv2.MORPH_RECT, ( MORPH, MORPH ) )

		closed = cv2.morphologyEx( edges, cv2.MORPH_CLOSE, kernel )

		contours, h = cv2.findContours( closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )

		for cont in contours:

			if cv2.contourArea( cont ) > 5000 :

				arc_len = cv2.arcLength( cont, True )

				approx = cv2.approxPolyDP( cont, 0.1 * arc_len, True )

				if ( len( approx ) == 4 ):
					IS_FOUND = 1
					#M = cv2.moments( cont )
					#cX = int(M["m10"] / M["m00"])
					#cY = int(M["m01"] / M["m00"])
					#cv2.putText(rgb, "Center", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

					pts_src = np.array( approx, np.float32 )

					h, status = cv2.findHomography( pts_src, pts_dst )
					out = cv2.warpPerspective( rgb, h, ( int( _width + _margin * 2 ), int( _height + _margin * 2 ) ) )

					cv2.drawContours( rgb, [approx], -1, ( 255, 0, 0 ), 2 )

				else : pass

		#cv2.imshow( 'closed', closed )
		#cv2.imshow( 'gray', gray )
		cv2.namedWindow( 'edges', cv2.CV_WINDOW_AUTOSIZE )
		cv2.imshow( 'edges', edges )

		cv2.namedWindow( 'rgb', cv2.CV_WINDOW_AUTOSIZE )
		cv2.imshow( 'rgb', rgb )

		if IS_FOUND :
			cv2.namedWindow( 'out', cv2.CV_WINDOW_AUTOSIZE )
			cv2.imshow( 'out', out )

		if cv2.waitKey(27) & 0xFF == ord('q') :
			break

		if cv2.waitKey(99) & 0xFF == ord('c') :
			saveImage.saveImage(out)

		time.sleep( DELAY )

	else :
		print "Stopped"
		break

if USE_CAM : video_capture.release()
cv2.destroyAllWindows()
//
//  TFViewController.h
//  test
//


#import <UIKit/UIKit.h>
#import <Vision/Vision.h>

NS_ASSUME_NONNULL_BEGIN
typedef void(^ReadHandler) (VNRequest*_Nonnullrequest,NSError*_Nullableerror);
@interface TFViewController : UIViewController
@property (nonatomic , copy)ReadHandler readHandler;


@end

NS_ASSUME_NONNULL_END

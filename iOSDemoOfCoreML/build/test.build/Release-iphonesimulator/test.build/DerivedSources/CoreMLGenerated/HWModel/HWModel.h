//
// HWModel.h
//
// This file was automatically generated and should not be edited.
//

#import <Foundation/Foundation.h>
#import <CoreML/CoreML.h>
#include <stdint.h>

NS_ASSUME_NONNULL_BEGIN


/// Model Prediction Input Type
API_AVAILABLE(macos(10.13), ios(11.0), watchos(4.0), tvos(11.0)) __attribute__((visibility("hidden")))
@interface HWModelInput : NSObject<MLFeatureProvider>

/// eval_input__0 as 1 x 32 x 32 3-dimensional array of doubles
@property (readwrite, nonatomic, strong) MLMultiArray * eval_input__0;
- (instancetype)init NS_UNAVAILABLE;
- (instancetype)initWithEval_input__0:(MLMultiArray *)eval_input__0;
@end


/// Model Prediction Output Type
API_AVAILABLE(macos(10.13), ios(11.0), watchos(4.0), tvos(11.0)) __attribute__((visibility("hidden")))
@interface HWModelOutput : NSObject<MLFeatureProvider>

/// op_to_store__0 as 1 x 1 x 1 3-dimensional array of doubles
@property (readwrite, nonatomic, strong) MLMultiArray * op_to_store__0;
- (instancetype)init NS_UNAVAILABLE;
- (instancetype)initWithOp_to_store__0:(MLMultiArray *)op_to_store__0;
@end


/// Class for model loading and prediction
API_AVAILABLE(macos(10.13), ios(11.0), watchos(4.0), tvos(11.0)) __attribute__((visibility("hidden")))
@interface HWModel : NSObject
@property (readonly, nonatomic, nullable) MLModel * model;
- (nullable instancetype)init;
- (nullable instancetype)initWithContentsOfURL:(NSURL *)url error:(NSError * _Nullable * _Nullable)error;
- (nullable instancetype)initWithConfiguration:(MLModelConfiguration *)configuration error:(NSError * _Nullable * _Nullable)error API_AVAILABLE(macos(10.14), ios(12.0), watchos(5.0), tvos(12.0)) __attribute__((visibility("hidden")));
- (nullable instancetype)initWithContentsOfURL:(NSURL *)url configuration:(MLModelConfiguration *)configuration error:(NSError * _Nullable * _Nullable)error API_AVAILABLE(macos(10.14), ios(12.0), watchos(5.0), tvos(12.0)) __attribute__((visibility("hidden")));

/**
    Make a prediction using the standard interface
    @param input an instance of HWModelInput to predict from
    @param error If an error occurs, upon return contains an NSError object that describes the problem. If you are not interested in possible errors, pass in NULL.
    @return the prediction as HWModelOutput
*/
- (nullable HWModelOutput *)predictionFromFeatures:(HWModelInput *)input error:(NSError * _Nullable * _Nullable)error;

/**
    Make a prediction using the standard interface
    @param input an instance of HWModelInput to predict from
    @param options prediction options
    @param error If an error occurs, upon return contains an NSError object that describes the problem. If you are not interested in possible errors, pass in NULL.
    @return the prediction as HWModelOutput
*/
- (nullable HWModelOutput *)predictionFromFeatures:(HWModelInput *)input options:(MLPredictionOptions *)options error:(NSError * _Nullable * _Nullable)error;

/**
    Make a prediction using the convenience interface
    @param eval_input__0 as 1 x 32 x 32 3-dimensional array of doubles:
    @param error If an error occurs, upon return contains an NSError object that describes the problem. If you are not interested in possible errors, pass in NULL.
    @return the prediction as HWModelOutput
*/
- (nullable HWModelOutput *)predictionFromEval_input__0:(MLMultiArray *)eval_input__0 error:(NSError * _Nullable * _Nullable)error;

/**
    Batch prediction
    @param inputArray array of HWModelInput instances to obtain predictions from
    @param options prediction options
    @param error If an error occurs, upon return contains an NSError object that describes the problem. If you are not interested in possible errors, pass in NULL.
    @return the predictions as NSArray<HWModelOutput *>
*/
- (nullable NSArray<HWModelOutput *> *)predictionsFromInputs:(NSArray<HWModelInput*> *)inputArray options:(MLPredictionOptions *)options error:(NSError * _Nullable * _Nullable)error API_AVAILABLE(macos(10.14), ios(12.0), watchos(5.0), tvos(12.0)) __attribute__((visibility("hidden")));
@end

NS_ASSUME_NONNULL_END

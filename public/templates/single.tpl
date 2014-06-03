<div>
    Episode (format 000, 001, 002, etc...)<input type="text" placeholder="042" id="singlesearch" ng-model="singlesearchvalue">
    <div>
        <div><counter></counter></div>
        <article data-ng-repeat="data in thedata">
            <secnow chez="data"></secnow>
        </article>
    </div>
</div>